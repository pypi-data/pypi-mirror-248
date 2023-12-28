import json
import requests

import numpy as np
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera.typing import Series, Index, DateTime
from typing import Callable, Optional

from .validator import Validator
from .. utils.calculation import get_diff_days, get_diff_month, set_diff, compare_diff_with_threshold
from .. utils import parameters, indicators, versioning, processes, get_not_canceled_objects


def _get_process_system_data(token: str, version_id: str) -> pd.DataFrame:

    process_rename_dict = {
        "88359fe3-4d1a-4bac-8fee-9ddd32eb9dc1": "permission_date", #РС
        "8b1663d9-a69d-40fd-8b3e-9f51b39d66a8": "construction_start_date", # НС
        "733fb7d0-0ec6-4223-846e-dcc0bebaaca9": "commition_date", #РВ
    }

    processes_dict = processes.get_process_statistics(
        token,
        version_id,
        processes=list(process_rename_dict.keys()),
        object_filter={"objectType": ["CONSTRUCTION_OBJECT"]},
        groupby="PROCESS",
    )
    combine_dates_df = processes.convert_process_statistics_dict_to_df(
        processes_dict,
        columns=[
            'constructionObject_id',
            'overallEnd',
            'status',
        ],
        index_name='constructionObject_id',
        process_rename_dict=process_rename_dict
    )
    return combine_dates_df

def _get_indicator_system_data(indicator_token: str, version_token: str) -> pd.DataFrame:
    version_df = indicators.get_versions(indicator_token)
    versions_release = version_df[version_df.title.str.startswith('Релиз')]
    release_version = versioning.get_release_version(version_token, versions_release.id.tolist())

    del version_df, versions_release
    resp = indicators.get_indicator_values(
        indicator_token,
        release_version,
        indicators=["po.production.total"],
        groupby=[
            "constructionObjectId",
            "itemTreeId"
        ],
        filter={
            "itemTreeId": [
                "76630097-e1b1-4787-b509-36e4a13c1490",
                "9f90fee4-22b0-4c75-b298-03b9af46a679",

                "4734c36c-9c27-44bc-82a1-1265267b0737",
                "05cacdf3-9de7-4bae-8916-59be9ef6c3c2",
                "ce719b53-3bf5-4c30-b8e5-7a1c8feaa4cb",
                "17d417b9-f6f1-44c2-b554-830e7a903274",
                "d3034170-b66f-4914-a2fd-e2cbc986038b",
                "e3bbb51d-07a1-44a0-a628-a1504f87ffe9",
            ]
        }
    )

    df = pd.DataFrame(resp.json()[0]['slices'])
    df.yearMonth = pd.to_datetime(df.yearMonth)
    df_first_date = df[df.amount > 0]
    df_first_date = df_first_date.sort_values(by=['constructionObjectId', 'yearMonth'], ascending=True)
    df_first_date = df_first_date.groupby('constructionObjectId').first()

    df_first_date = df_first_date.drop(columns='itemTreeId')
    df_first_date.columns = 'first_spend_' + df_first_date.columns
    return df_first_date


### Проверки
# методы проверок можно полодить в класс схемы (регистрация не нужна, т.к. схемы мы не сериализуем)
@extensions.register_check_method()
def check_sdp_date_less_permission_date(df, *, threshold: float):
    diff = get_diff_days(df['sdp_overallEnd'], df['permission_date_overallEnd'])
    set_diff(df, diff)
    result = compare_diff_with_threshold(diff, pd.Series.gt, threshold, exclude_na=True)
    return result

@extensions.register_check_method()
def check_permission_date_less_construction_start_date(df, *, threshold: float):
    diff = get_diff_days(df['permission_date_overallEnd'], df['construction_start_date_overallEnd'])
    set_diff(df, diff)
    result = compare_diff_with_threshold(diff, pd.Series.gt, threshold, exclude_na=True)
    return result

@extensions.register_check_method()
def check_diff_commition_date_construction_start_date(df, *, threshold: float):
    diff = get_diff_month(df['construction_start_date_overallEnd'], df['commition_date_overallEnd']) / 12
    set_diff(df, diff)
    result = compare_diff_with_threshold(diff, pd.Series.ge, threshold, exclude_na=True)
    return result

@extensions.register_check_method()
def check_diff_commition_date_permission_date(df, *, threshold: tuple[float, float]):
    diff = get_diff_month(df['permission_date_overallEnd'], df['commition_date_overallEnd']) / 12
    set_diff(df, diff)
    ge_year = compare_diff_with_threshold(diff, pd.Series.ge, threshold[0], exclude_na=True)
    lt_3_5_years = compare_diff_with_threshold(diff, pd.Series.lt, threshold[1], exclude_na=True)
    return ge_year & lt_3_5_years

@extensions.register_check_method()
def check_first_spend_is_in_construction_start_month(df, *,  threshold: float):
    diff = get_diff_month(df['first_spend_yearMonth'], df['construction_start_date_overallEnd'])
    set_diff(df, diff)
    result = compare_diff_with_threshold(diff, pd.Series.eq, threshold, exclude_na=True)
    return result


class Schema(pa.DataFrameModel):
    parcel_id: Series[str] = pa.Field(nullable=False)
    parcel_canceled: Series[bool] = pa.Field(ne=True)
    sdp_overallEnd: Series[DateTime] = pa.Field(nullable=True)
    permission_date_overallEnd: Series[DateTime] = pa.Field(nullable=False)
    construction_start_date_overallEnd: Series[DateTime] = pa.Field(nullable=False)
    commition_date_overallEnd: Series[DateTime] = pa.Field(nullable=False)
    first_spend_yearMonth: Series[DateTime] = pa.Field(nullable=True)
    first_spend_amount: Series[float] = pa.Field(nullable=True)
    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

def _make_check_past_milestone_status(
    tag_date: str,
    tag_status: str,
    check_name: str
) -> Callable[[pd.DataFrame], pd.Series]:
    def check_past_milestone_status(df, *, now_datetime: pd.Timestamp):
        diff = get_diff_days(df[tag_date], now_datetime)
        set_diff(df, diff, check_name)

        compare_dates = compare_diff_with_threshold(diff, pd.Series.gt, threshold=0, exclude_na=False)
        compare_status = df[tag_status] != 'COMPLETE'
        return ~(compare_dates & compare_status)
    return check_past_milestone_status


class Validator_co_milestone_dates(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens

    def _generate_checks_past_milestone_status(self, now_datetime: pd.Timestamp) -> None:
        check_tags = ['sdp', 'permission_date', 'construction_start_date', 'commition_date']

        for tag in check_tags:
            check_name = f"check_past_{tag}_status"
            factory_args={
                'tag_date': f'{tag}_overallEnd',
                'tag_status': f'{tag}_status',
                'check_name': check_name
            }
            self._create_check(_make_check_past_milestone_status, factory_args, check_name)
            self._add_check_to_schema(check_name, check_args={'now_datetime': now_datetime})

    def _generate_checks(self, now_datetime: pd.Timestamp) -> None:
        if len(self.schema.__extras__) == 0:
            self._generate_checks_past_milestone_status(now_datetime)

            self._add_check_to_schema('check_sdp_date_less_permission_date', check_args={'threshold': 0})
            self._add_check_to_schema('check_permission_date_less_construction_start_date', check_args={'threshold': 0})
            self._add_check_to_schema('check_diff_commition_date_construction_start_date', check_args={'threshold': 1})
            self._add_check_to_schema('check_diff_commition_date_permission_date', check_args={'threshold': (1, 3.5)})
            self._add_check_to_schema('check_first_spend_is_in_construction_start_month', check_args={'threshold': 0})


    def get_data(
        self,
        sdp_df: pd.DataFrame,
        version_id: str
    ) -> tuple[pd.DataFrame, dict[str, list[str]]]:
        constr_objs_df = parameters.get_construction_objects(self.tokens['parameters'], version_id)
        not_canceled_objs = get_not_canceled_objects(constr_objs_df, return_index=False)[['parcel_id']]

        parcel_series = parameters.get_parcels(self.tokens['parameters'], version_id)['canceled']
        parcel_series = parcel_series.rename('parcel_canceled')

        process_data = _get_process_system_data(self.tokens['processes'], version_id)
        indicator_data = _get_indicator_system_data(self.tokens['indicators'], self.tokens['versioning'])

        result_df = not_canceled_objs.merge(sdp_df, how='left', left_on='parcel_id', right_index=True)
        result_df = result_df.merge(parcel_series, how='left', left_on='parcel_id', right_index=True)
        result_df.parcel_canceled = result_df.parcel_canceled.replace(np.nan, False)

        result_df = result_df.join(process_data, how='left')
        result_df = result_df.join(indicator_data, how='left')

        lost_objs = {
            'process_system': list(set(not_canceled_objs.index) - set(process_data.index)),
            'indicator_system': list(set(not_canceled_objs.index) - set(indicator_data.index))
        }
        return result_df, lost_objs

    def validate(self, df: pd.DataFrame, lost_objs: Optional[dict[str, list[str]]]) -> Optional[pd.DataFrame]:
        now_datetime = pd.Timestamp.now()
        self._generate_checks(now_datetime)
        result_df = super().validate(df)

        result_lost_objs = pd.DataFrame()
        if lost_objs is not None:
            for system in lost_objs.keys():
                lost_obj_sys = pd.DataFrame(columns=result_df.columns)
                lost_obj_sys.object_index = lost_objs[system]
                lost_obj_sys.schema_context = 'InputData'
                lost_obj_sys.check_name = f'check_missing_objects_{system}'
                result_lost_objs = pd.concat([result_lost_objs, lost_obj_sys], axis=0)

        if result_df is not None:
            result_df = result_df.drop(
                index=result_df[
                    (result_df.check_name == 'not_nullable')
                    & result_df.object_index.isin(lost_objs.get('process_system'))
                ].index
            )
            result_df = pd.concat([result_df, result_lost_objs], axis=0, ignore_index=True)
            result_df.insert(0, column='test_name', value='test_co_milestone_dates')
            result_df.insert(0, column='datetime', value=now_datetime)
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])
        return result_df
