import numpy as np
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from pandera.typing import Series, Index, DateTime
from typing import Optional

from .validator import Validator
from .. utils import parameters, processes, get_not_canceled_objects


def _get_process_system_sdp_milestone(token: str, version_id: str) -> pd.DataFrame:
    processes_dict = processes.get_process_statistics(
        token,
        version_id,
        processes=['14e74f88-6d10-4a05-b072-507d1a5dddd1'],
        object_filter={"objectType": ["PARCEL"]},
        groupby="PROCESS",
    )
    df = processes.convert_process_statistics_dict_to_df(
        processes_dict,
        columns=[
            'parcel_id',
            'overallEnd',
            'status',
        ],
        index_name='parcel_id',
        process_rename_dict={
            '14e74f88-6d10-4a05-b072-507d1a5dddd1': 'sdp'
        }
    )
    return df

class Schema(pa.DataFrameModel):
    sdp_overallEnd: Series[DateTime] = pa.Field(nullable=False)
    id: Index[str] = pa.Field(check_name=True, unique=True)

    class Config:
        coerce = True

class Validator_parcel_milestone_dates(Validator):
    def __init__(self, tokens: dict[str, str]):
        self.schema = Schema
        self.tokens = tokens

    def get_data(self, version_id: str) -> tuple[pd.DataFrame, dict[str, list[str]]]:
        not_canceled_objs = get_not_canceled_objects(
            parameters.get_parcels(self.tokens['parameters'], version_id)
        )

        spd_date_status = _get_process_system_sdp_milestone(self.tokens['processes'], version_id)

        result_df = pd.DataFrame(index=not_canceled_objs)
        result_df = result_df.join(spd_date_status, how='left')

        return result_df

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        result_df = super().validate(df)

        if result_df is not None:
            result_df.insert(0, column='test_name', value='test_parcel_milestone_dates')
            result_df.insert(0, column='datetime', value=pd.Timestamp.now())
            result_df.insert(len(result_df.columns), column='obj_count', value=df.shape[0])

        return result_df
