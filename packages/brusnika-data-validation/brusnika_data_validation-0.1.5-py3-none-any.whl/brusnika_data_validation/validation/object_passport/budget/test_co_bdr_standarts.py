import json
import re
import requests
from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera.typing import Series, Index, DateTime

from .... validation import Validator
from .... utils.calculation import get_abs_diff, get_relative_diff, set_diff, compare_diff_with_threshold
from .... utils import parameters, bluebook


def _get_region_code(code: str, region_codes: list[str], reg_contour_codes: dict[str, list[str]]) -> Optional[str]:
    if code in region_codes:
        return code

    # regions_needed = list(reg_contour_codes.keys() & set(region_codes))
    for region_key in reg_contour_codes.keys():
        region_contours = reg_contour_codes[region_key]
        if code in region_contours:
            return region_key

    return None

def _get_add_dataset_area_statistics(
    param_token: str,
    bluebook_token: str,
    version_id: str,
):
    standarts_df = bluebook.get_standard_cost(bluebook_token)
    area_df = parameters.get_area_statistics_sfa(
        param_token, version_id
        ).set_index('constructionObject_id')[['area', 'contour_id', 'grade_id']]
    contours_df = parameters.get_contours(param_token)
    grades_df = parameters.get_grades(param_token)

    reg_contour_codes = {'reg': ['nsk', 'ekb', 'krg', 'oms', 'tmn']} #вынести в маппинги?
    contours_df['region_code'] = contours_df.contour_code.apply(
        lambda code: _get_region_code(code, standarts_df.index.levels[0].tolist(), reg_contour_codes)
    )

    grades_df.grade = grades_df.grade.str.replace('+', '_PLUS')

    add_df = area_df.merge(contours_df, how='left', left_on='contour_id', right_index=True)
    add_df = add_df.merge(grades_df, how='left', left_on='grade_id', right_index=True)
    add_df = add_df.merge(standarts_df, how='left', left_on=['region_code', 'grade'], right_index=True)
    return add_df

def _get_needed_columns(mapping: dict):
    df = pd.DataFrame.from_dict(mapping, orient='index')
    columns = df[~df.is_expense.isna()].index
    del df
    return columns.tolist()

def _calculate_relative_parameters(df: pd.DataFrame, param_tags: list[str], mapping: dict) -> pd.DataFrame:
    result_df = df.copy(deep=True)

    for tag in param_tags:
        if mapping[tag]['is_expense']:
            result_df[tag] = np.abs(result_df[tag])

    result_df['land_to_revenue'] = result_df['fa_costs_land'] / result_df['fa_revenue'] * 100 # %
    result_df['revenue_to_construction'] = result_df['fa_revenue'] / result_df['fa_costs_production_construction']
    result_df['sga_to_revenue'] = result_df['fa_sga'] / result_df['fa_revenue'] * 100 # %

    result_df['gross_margin_to_revenue'] = result_df['fa_gross_margin'] / result_df['fa_revenue'] * 100 # %
    result_df['ebitda_to_revenue'] = result_df['fa_ebitda'] / result_df['fa_revenue'] * 100 # %
    result_df['net_profit_to_revenue'] = result_df['fa_net_profit'] / result_df['fa_revenue'] * 100 # %

    result_df[param_tags] = result_df[param_tags].div(result_df.area, axis=0)

    result_df = result_df.replace([np.inf, -np.inf], np.nan)
    return result_df


@extensions.register_check_method()
def check_zero_standart_fa_costs_facilities(df, *, tag: str, standart_tag: str, threshold: float):
    result_series = pd.Series(index=df.index, dtype='bool')
    zero_standard_mask = (df[standart_tag] == 0)

    diff = pd.Series(index=df.index, dtype='float')
    diff.loc[zero_standard_mask] = get_abs_diff(df.loc[zero_standard_mask, tag], df.loc[zero_standard_mask, standart_tag])
    set_diff(df, diff)
    result_series.loc[zero_standard_mask] = compare_diff_with_threshold(diff, pd.Series.lt, threshold, exclude_na=True) # threshold надо выносить в маппинг?
    return result_series

@extensions.register_check_method()
def check_standart_fa_costs_facilities(df, *, tag: str, standart_tag: str, threshold: float):
    result_series = pd.Series(index=df.index, dtype='bool')
    zero_standard_mask = (df[standart_tag] == 0)

    diff = pd.Series(index=df.index, dtype='float')
    diff.loc[~zero_standard_mask] = get_relative_diff(df.loc[~zero_standard_mask, tag], df.loc[~zero_standard_mask, standart_tag])
    set_diff(df, diff)
    result_series.loc[~zero_standard_mask] = compare_diff_with_threshold(diff, pd.Series.lt, threshold, exclude_na=True)
    return result_series

class Schema(pa.DataFrameModel):
    land_to_revenue: Series[float] = pa.Field(nullable=False, gt=0)
    revenue_to_construction: Series[float] = pa.Field(nullable=False, gt=0) #КДС
    sga_to_revenue: Series[float] = pa.Field(nullable=False, gt=0)
    gross_margin_to_revenue: Series[float] = pa.Field(nullable=False, gt=0)
    ebitda_to_revenue: Series[float] = pa.Field(nullable=False, gt=0)
    net_profit_to_revenue: Series[float] = pa.Field(nullable=False, gt=0)

    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

def _make_check_standart(
    tag: str,
    standart_tag: str,
    check_is_relative: bool,
    check_name: str,
    is_percent: Optional[bool]
) -> Callable[[pd.DataFrame], pd.Series]:
    def check_standart(df, *, threshold: float):
        standart_value = df[standart_tag].copy(deep=True)
        if is_percent:
            standart_value *= 100

        diff = get_abs_diff(df[tag], standart_value)
        if check_is_relative:
            diff = get_relative_diff(df[tag], standart_value) * 100
        set_diff(df, diff, check_name)

        result = compare_diff_with_threshold(diff, pd.Series.lt, threshold=threshold, exclude_na=True)
        return result
    return check_standart


class Validator_co_bdr_standarts(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens
        self.mapping_standarts = {}

    def _generate_checks_standart(self) -> None:
        for tag in self.mapping_standarts.keys():
            if self.mapping_standarts[tag].get('standart_is_zero'):
                continue
            check_name = f"check_standart_{tag}"
            factory_args={
                'tag': tag,
                'standart_tag': self.mapping_standarts[tag]['standart'],
                'check_is_relative': self.mapping_standarts[tag]['check_is_relative'],
                'check_name': check_name,
                'is_percent': self.mapping_standarts[tag].get('is_percent')
            }
            self._create_check(_make_check_standart, factory_args, check_name)
            self._add_check_to_schema(check_name, check_args={'threshold': self.mapping_standarts[tag]['threshold']})

    def _generate_checks(self) -> None:
        if len(self.schema.__extras__) == 0:
            self._generate_checks_standart()

            tag = 'fa_costs_facilities'
            standart_tag = self.mapping_standarts[tag]['standart']
            self._add_check_to_schema('check_zero_standart_fa_costs_facilities', check_args={
                'tag': tag,
                'standart_tag': standart_tag,
                'threshold': 0.1,
            })
            self._add_check_to_schema('check_standart_fa_costs_facilities', check_args={
                'tag': tag,
                'standart_tag': standart_tag,
                'threshold': self.mapping_standarts[tag]['threshold'],
            })

    def get_data(
        self,
        budget_df: pd.DataFrame,
        version_id: str,
        mapping_filename: str = 'mapping.json'
    ) -> pd.DataFrame:
        with open(mapping_filename, 'r') as f:
            mapping = json.load(f)
        self.mapping_standarts = mapping["Эталоны"]
        columns = _get_needed_columns(self.mapping_standarts)
        columns = list(set(columns) & set(budget_df.columns))

        add_df = _get_add_dataset_area_statistics(self.tokens['parameters'], self.tokens['bluebook'], version_id)
        result_df = budget_df[columns].join(add_df, how='left')

        result_df = _calculate_relative_parameters(result_df, columns, self.mapping_standarts)

        return result_df

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self._generate_checks()

        result_df = super().validate(df)

        if result_df is not None:
            result_df.insert(0, column='test_name', value='test_co_bdr_standarts')
            result_df.insert(0, column='datetime', value=pd.Timestamp.now())
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])

        return result_df
