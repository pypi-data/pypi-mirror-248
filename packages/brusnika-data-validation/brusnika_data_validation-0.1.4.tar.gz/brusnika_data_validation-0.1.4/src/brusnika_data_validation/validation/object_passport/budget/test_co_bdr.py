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
from .... utils.calculation import calc_sum_cols, get_abs_diff, set_diff, compare_diff_with_threshold
from .... utils import parameters, indicators, get_not_canceled_objects


class Schema(pa.DataFrameModel):
    fa_revenue: Series[float] = pa.Field(nullable=False, gt=0)

    # move to test_co_production
    fa_costs_production_construction: Series[float] = pa.Field(nullable=True)
    fa_costs_production_design: Series[float] = pa.Field(nullable=True)
    fa_costs_production_infrastructure: Series[float] = pa.Field(nullable=True)
    fa_costs_production: Series[float] = pa.Field(nullable=True)

    fa_costs_land: Series[float] = pa.Field(nullable=False, lt=0)
    fa_costs_facilities: Series[float] = pa.Field(nullable=False, le=0) # Расходы на инфраструктуру >=0
    fa_costs_warranty: Series[float] = pa.Field(nullable=False, lt=0)
    # Расходы на ввод и содержание (пока отсутствуют в парам. системе le=0)
    fa_costs: Series[float] = pa.Field(nullable=False, lt=0)

    fa_gross_margin: Series[float] = pa.Field(nullable=False, gt=0)

    fa_sga: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_developer_management: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_design_management: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_marketing: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_sales_management: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_brokerage: Series[float] = pa.Field(nullable=False, lt=0)
    fa_sga_hci: Series[float] = pa.Field(nullable=False, lt=0)

    fa_internal_expenses: Series[float] = pa.Field(nullable=False, lt=0)

    fa_ebitda: Series[float] = pa.Field(nullable=False, gt=0)

    #fa_interest 	# % банку (отсутсвует в сете)
    fa_expenses: Series[float] = pa.Field(nullable=False, lt=0)

    fa_taxes_income_tax: Series[float] = pa.Field(nullable=False, lt=0)
    fa_net_profit: Series[float] = pa.Field(nullable=False, gt=0)

    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

def _make_check_sum_param_tags(tag: str, term_cols: list[str], check_name: str) -> Callable:
    def check_sum(df, *, threshold: float):
        sum_value = calc_sum_cols(df, term_cols)
        diff = get_abs_diff(df[tag], sum_value)
        set_diff(df, diff, check_name)
        result = compare_diff_with_threshold(diff, pd.Series.lt, threshold=threshold, exclude_na=True)
        return result
    return check_sum


class Validator_co_bdr(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens

        self.mapping_param_sum = {}
        self.mapping_standarts = {}

    def _generate_checks_sum_param_tags(self) -> None:
        for tag in self.mapping_param_sum.keys():
            check_name = f"check_sum_{tag}"
            factory_args={
                'tag': tag,
                'term_cols': self.mapping_param_sum[tag],
                'check_name': check_name,
            }
            self._create_check(_make_check_sum_param_tags, factory_args, check_name)
            self._add_check_to_schema(check_name, check_args={'threshold': 1})

    def _generate_checks(self) -> None:
        if len(self.schema.__extras__) == 0:
            self._generate_checks_sum_param_tags()

    def get_data(
        self,
        version_id: str,
        mapping_filename: str = 'mapping.json'
    ) -> pd.DataFrame:
        with open(mapping_filename, 'r') as f:
            mapping = json.load(f)
        self.mapping_param_sum = mapping["Суммы по стакану"]
        self.mapping_standarts = mapping["Эталоны"]

        not_canceled_objs = get_not_canceled_objects(
            parameters.get_construction_objects(
                self.tokens['parameters'], version_id, all=False, construction=True
            )
        )
        param_fin_data = parameters.get_financial_data_root_items(self.tokens['parameters'], version_id)

        result_df = pd.DataFrame(index = not_canceled_objs)
        result_df = result_df.join(param_fin_data, how='left')

        return result_df

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self._generate_checks()

        result_df = super().validate(df)

        if result_df is not None:
            result_df.insert(0, column='test_name', value='test_co_bdr')
            result_df.insert(0, column='datetime', value=pd.Timestamp.now())
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])

        return result_df
