import json
import re
import requests

import numpy as np
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera.typing import Series, Index
from typing import Callable, Optional

from ... validation.validator import Validator
from ... utils import parameters, indicators, get_not_canceled_objects
from ... utils.calculation import get_abs_diff, set_diff, compare_diff_with_threshold


def _get_indicator_system_data(token: str, version_id: str) -> pd.DataFrame:
    resp_inds = indicators.get_indicator_values(
        token,
        version_id,
        indicators=[
            "po.production.total",
            "po.production.construction",
            "po.production.design",
            "po.production.infrastructure",

            "po.production.completion"
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
    po_production_total: Series[float] = pa.Field(nullable=False, gt=0)
    po_production_construction: Series[float] = pa.Field(nullable=False, gt=0)
    po_production_design: Series[float] = pa.Field(nullable=False, gt=0)
    po_production_infrastructure: Series[float] = pa.Field(nullable=False, gt=0)

    po_production_completion: Series[float] = pa.Field(nullable=False, in_range={"min_value": 0.999, "max_value": 1.001})

    fa_costs_production_construction: Series[float] = pa.Field(nullable=False, lt=0)
    fa_costs_production_design: Series[float] = pa.Field(nullable=False, lt=0)
    fa_costs_production_infrastructure: Series[float] = pa.Field(nullable=False, lt=0)
    fa_costs_production: Series[float] = pa.Field(nullable=False, lt=0)

    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

def _make_check_param_eq_sum_ind(param_tag: str, ind_tag: str, check_name: str) -> Callable:
    def check_param_eq_sum_ind(df, *, threshold: float):
        diff = get_abs_diff(np.abs(df[param_tag]), df[ind_tag])
        set_diff(df, diff, check_name)
        result = compare_diff_with_threshold(diff, pd.Series.lt, threshold=threshold, exclude_na=True)
        return result
    return check_param_eq_sum_ind

class Validator_co_production(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens

        self.fin_tags = [
            "fa.costs.production.construction",
            "fa.costs.production.design",
            "fa.costs.production.infrastructure",
            "fa.costs.production"
        ]
        self.mapping_param_ind = {
            "fa_costs_production_construction": "po_production_construction",
            "fa_costs_production_design": "po_production_design",
            "fa_costs_production_infrastructure": "po_production_infrastructure",
            "fa_costs_production": "po_production_total"
        }

    def _generate_checks_param_eq_sum_ind(self) -> None:
        for tag in self.mapping_param_ind.keys():
            check_name = f"check_param_eq_sum_ind_{tag}"
            factory_args={
                'param_tag': tag,
                'ind_tag': self.mapping_param_ind[tag],
                'check_name': check_name,
            }
            self._create_check(_make_check_param_eq_sum_ind, factory_args, check_name)
            self._add_check_to_schema(check_name, check_args={'threshold': 1})

    def _generate_checks(self) -> None:
        if len(self.schema.__extras__) == 0:
            self._generate_checks_param_eq_sum_ind()

    def get_data(self, version_id: str) -> pd.DataFrame:
        not_canceled_objs = get_not_canceled_objects(
            parameters.get_construction_objects(self.tokens['parameters'], version_id)
        )
        param_fin_data = parameters.get_financial_data_root_items(self.tokens['parameters'], version_id, self.fin_tags)
        param_fin_data = param_fin_data[list(map(lambda x: re.sub(r'[-.]', '_', x), self.fin_tags))]

        indicator_data = _get_indicator_system_data(self.tokens['indicators'], version_id)

        result_df = pd.DataFrame(index=not_canceled_objs)
        result_df = result_df.join(param_fin_data, how='left')
        result_df = result_df.join(indicator_data, how='left')

        return result_df

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self._generate_checks()

        result_df = super().validate(df)

        if result_df is not None:
            result_df.insert(0, column='test_name', value='test_co_production')
            result_df.insert(0, column='datetime', value=pd.Timestamp.now())
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])

        return result_df
