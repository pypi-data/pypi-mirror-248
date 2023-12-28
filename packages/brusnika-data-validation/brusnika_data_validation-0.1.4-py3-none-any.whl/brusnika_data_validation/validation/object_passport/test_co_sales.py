import json
import re
import requests

import numpy as np
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera.typing import Series, Index
from typing import Optional, Callable

from ... validation.validator import Validator
from ... utils.calculation import get_abs_diff_fillna, set_diff, compare_diff_with_threshold, calc_sum_cols, get_abs_diff
from ... utils import parameters, indicators, get_not_canceled_objects

def _get_sfa(token: str, version_id: str) -> pd.DataFrame:
    df = parameters.get_area_statistics_sfa(token, version_id, groupby=["CONSTRUCTION_OBJECT", "PREMISE_KIND"])
    result_df = pd.pivot_table(df, index='constructionObject_id', columns='premiseKind', values='area', aggfunc=np.sum)
    result_df.columns = 'sfa_' + result_df.columns.str.lower()
    result_df.columns.name = None

    common_area_df = parameters.get_area_statistics_sfa(token, version_id)
    sfa_common = common_area_df.set_index('constructionObject_id').area
    sfa_common.name = 'sfa'
    result_df = pd.concat([result_df, sfa_common], axis=1)

    del df, common_area_df, sfa_common
    return result_df

def _get_indicator_system_data_premises_kind(token: str, version_id: str) -> pd.DataFrame:
    resp_inds = indicators.get_indicator_values(
        token,
        version_id,
        indicators=[
            "ss.sales.revenue",
            "ss.sales.area-total",
        ],
        groupby=[
            "constructionObjectId",
            "premisesKind"
        ]
    )
    indicator_dfs = indicators.convert_indicator_values_to_dfs_dict(
        resp_inds,
        columns=['constructionObjectId', 'premisesKind', 'yearMonth', 'amount']
    )

    indicator_calc_dfs = {}
    for indicator in indicator_dfs.keys():
        df = pd.pivot_table(indicator_dfs[indicator], index='constructionObjectId', columns='premisesKind', values='amount', aggfunc=np.sum)
        df.columns = indicator + '_' + df.columns
        indicator_calc_dfs.update({indicator: df})

    combine_ind_df = pd.concat(indicator_calc_dfs.values(), axis=1)
    return combine_ind_df

def _get_indicator_system_data_common_tags(token: str, version_id: str) -> pd.DataFrame:
    resp_inds = indicators.get_indicator_values(
        token,
        version_id,
        indicators=[
            "ss.sales.revenue",
            "ss.sales.area-total",
            "ss.sales.sales-percent",
        ],
        groupby=["constructionObjectId"]
    )
    indicator_dfs = indicators.convert_indicator_values_to_dfs_dict(
        resp_inds,
        columns=['constructionObjectId', 'yearMonth', 'amount']
    )

    indicator_calc_dfs = {}
    for indicator in indicator_dfs.keys():
        calc_series = indicator_dfs[indicator].groupby(by='constructionObjectId').amount.sum()
        calc_series.name = indicator
        indicator_calc_dfs.update({indicator: calc_series})

    combine_ind_df = pd.concat(indicator_calc_dfs.values(), axis=1)
    return combine_ind_df


class Schema(pa.DataFrameModel):
    # fa_revenue: Series[float] = pa.Field(nullable=True)
    fa_revenue_residential: Series[float] = pa.Field(nullable=True)
    fa_revenue_commercial: Series[float] = pa.Field(nullable=True)
    fa_revenue_parking: Series[float] = pa.Field(nullable=True)
    fa_revenue_storage: Series[float] = pa.Field(nullable=True)

    sfa: Series[float] = pa.Field(nullable=False, gt=0)
    sfa_residential: Series[float] = pa.Field(nullable=True)
    sfa_commercial: Series[float] = pa.Field(nullable=True)
    sfa_parking: Series[float] = pa.Field(nullable=True)
    sfa_storage: Series[float] = pa.Field(nullable=True)

    ss_sales_revenue: Series[float] = pa.Field(nullable=False, gt=0)
    ss_sales_revenue_residential: Series[float] = pa.Field(nullable=True)
    ss_sales_revenue_commercial: Series[float] = pa.Field(nullable=True)
    ss_sales_revenue_parking: Series[float] = pa.Field(nullable=True)
    ss_sales_revenue_storage: Series[float] = pa.Field(nullable=True)

    ss_sales_area_total: Series[float] = pa.Field(nullable=False, gt=0)
    ss_sales_area_total_residential: Series[float] = pa.Field(nullable=True)
    ss_sales_area_total_commercial: Series[float] = pa.Field(nullable=True)
    ss_sales_area_total_parking: Series[float] = pa.Field(nullable=True)
    ss_sales_area_total_storage: Series[float] = pa.Field(nullable=True)

    ss_sales_sales_percent: Series[float] = pa.Field(nullable=False, in_range={"min_value": 0.999, "max_value": 1.001})

    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

def _make_check_param_eq_sum_ind(param_tag: str, ind_tag: str, check_name: str) -> Callable:
    def check_param_eq_sum_ind(df, *, threshold: float):
        diff = get_abs_diff_fillna(df[param_tag], df[ind_tag], 0)
        set_diff(df, diff, check_name)
        result = compare_diff_with_threshold(diff, pd.Series.lt, threshold=threshold, exclude_na=True)
        return result
    return check_param_eq_sum_ind

def _make_check_revenue_notna_exist_area(area_tag: str, revenue_tag: str, check_name: str) -> Callable:
    def check_revenue_notna_exist_area(df):
        set_diff(df, pd.Series(data=check_name, index=df.index), check_name)
        return ~((df[area_tag] > 0) & ~(df[revenue_tag] > 0))
    return check_revenue_notna_exist_area

def _make_check_area_notna_exist_revenue(area_tag: str, revenue_tag: str, check_name: str) -> Callable:
    def check_area_notna_exist_revenue(df):
        set_diff(df, pd.Series(data=check_name, index=df.index), check_name)
        return ~((df[revenue_tag] > 0) & ~(df[area_tag] > 0))
    return check_area_notna_exist_revenue

def _make_check_sum_ind_tags(tag: str, term_cols: list[str], check_name: str) -> Callable:
    def check_sum(df, *, threshold: float):
        sum_value = calc_sum_cols(df, term_cols)
        diff = get_abs_diff(df[tag], sum_value)
        set_diff(df, diff, check_name)
        result = compare_diff_with_threshold(diff, pd.Series.lt, threshold=threshold, exclude_na=True)
        return result
    return check_sum

class Validator_co_sales(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens
        self.fin_tags = [
            "fa.revenue",
            "fa.revenue.residential",
            "fa.revenue.commercial",
            "fa.revenue.parking",
            "fa.revenue.storage",
        ]
        self.premise_types = [
            'residential',
            'commercial',
            'parking',
            'storage',
        ]
        self.mapping_param_ind_parts = {
            'fa_revenue_': 'ss_sales_revenue_',
            'sfa_': 'ss_sales_area_total_',
        }
        self.mapping_area_revenue_parts = {
            'sfa_': 'fa_revenue_',
            'ss_sales_area_total_': 'ss_sales_revenue_',
        }

    def _generate_checks_param_eq_sum_ind(self) -> None:
        for param_tag_part, ind_tag_part in self.mapping_param_ind_parts.items():
            for type in self.premise_types:
                param_tag = f'{param_tag_part}{type}'
                ind_tag = f'{ind_tag_part}{type}'
                check_name = f"check_param_eq_sum_ind_{param_tag}"
                factory_args = {
                    'param_tag': param_tag,
                    'ind_tag': ind_tag,
                    'check_name': check_name,
                }
                self._create_check(_make_check_param_eq_sum_ind, factory_args, check_name)
                self._add_check_to_schema(check_name, check_args={'threshold': 1})

    def _generate_checks_revenue_notna_exist_area(self) -> None:
        for type in self.premise_types:
            area_tag_part, revenue_tag_part = 'sfa_', 'fa_revenue_'
            # for area_tag_part, revenue_tag_part in self.mapping_area_revenue_parts.items():
            area_tag = f'{area_tag_part}{type}'
            revenue_tag = f'{revenue_tag_part}{type}'
            check_name = f"check_{revenue_tag}_notna_exist_area"
            factory_args = {
                'area_tag': area_tag,
                'revenue_tag': revenue_tag,
                'check_name': check_name,
            }
            self._create_check(_make_check_revenue_notna_exist_area, factory_args, check_name)
            self._add_check_to_schema(check_name)

    def _generate_checks_area_notna_exist_revenue(self) -> None:
        for type in self.premise_types:
            area_tag_part, revenue_tag_part = 'sfa_', 'fa_revenue_'
            # for area_tag_part, revenue_tag_part in self.mapping_area_revenue_parts.items():
            area_tag = f'{area_tag_part}{type}'
            revenue_tag = f'{revenue_tag_part}{type}'
            check_name = f"check_{area_tag}_notna_exist_revenue"
            factory_args = {
                'area_tag': area_tag,
                'revenue_tag': revenue_tag,
                'check_name': check_name,
            }
            self._create_check(_make_check_area_notna_exist_revenue, factory_args, check_name)
            self._add_check_to_schema(check_name)

    def _generate_checks_sum_ind_tags(self) -> None:
        # for tag in self.mapping_ind_sum.keys():
        for tag in ['ss_sales_revenue', 'ss_sales_area_total']:
            check_name = f"check_sum_{tag}"
            factory_args = {
                'tag': tag,
                # 'term_cols': self.mapping_ind_sum[tag],
                'term_cols': pd.Series(self.premise_types).apply(lambda x: f'{tag}_{x}').tolist(),
                'check_name': check_name,
            }
            self._create_check(_make_check_sum_ind_tags, factory_args, check_name)
            self._add_check_to_schema(check_name, check_args={'threshold': 1e-2})

    def _generate_checks(self, df: pd.DataFrame) -> None:
        if len(self.schema.__extras__) == 0:
            self._generate_checks_param_eq_sum_ind()
            self._generate_checks_revenue_notna_exist_area()
            self._generate_checks_area_notna_exist_revenue()
            self._generate_checks_sum_ind_tags()

    def get_data(
        self,
        version_id: str
    ) -> pd.DataFrame:
        not_canceled_objs = get_not_canceled_objects(
            parameters.get_construction_objects(
                self.tokens['parameters'], version_id, all=False, construction=True
            )
        )
        param_fin_data = parameters.get_financial_data_root_items(self.tokens['parameters'], version_id, self.fin_tags)
        param_fin_data = param_fin_data[list(map(lambda x: re.sub(r'[-.]', '_', x), self.fin_tags))]
        area_df = _get_sfa(self.tokens['parameters'], version_id)

        indicator_data = _get_indicator_system_data_premises_kind(self.tokens['indicators'], version_id)
        indicator_data_common = _get_indicator_system_data_common_tags(self.tokens['indicators'], version_id)

        result_df = pd.DataFrame(index=not_canceled_objs)
        result_df = result_df.join(param_fin_data, how='left')
        result_df = result_df.join(area_df, how='left')
        result_df = result_df.join(indicator_data, how='left')
        result_df = result_df.join(indicator_data_common, how='left')
        return result_df

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self._generate_checks(df)

        result_df = super().validate(df)

        if result_df is not None:
            result_df.insert(0, column='test_name', value='test_co_sales')
            result_df.insert(0, column='datetime', value=pd.Timestamp.now())
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])

        return result_df
