import re
import requests
from typing import Any

import pandas as pd


URL_ERP_PROCESSES = 'https://erp-core.brusnika.ru/processes/v3'

def get_process_statistics(
        token: str,
        version_id: str,
        processes: list[str],
        object_filter: dict[str, list[str]] = {},
        groupby: str = "PROCESS",
    ) -> dict[str, Any]:
    """
    processes: list[str]
    A list of processes IDs

    Return a dict of response json with key is processes ID.
    """
    url = f'{URL_ERP_PROCESSES}/versions/{version_id}/process-statistics'
    request_body = {
        "objectFilter": [object_filter],
        "periodFilter": {
            "since": None,
            "until": None
        },
        "groupBy": groupby
    }

    processes_dict = {}
    
    for process_id in processes:
        request_body['objectFilter'][0].update({"process": [process_id]})
        resp = requests.post(url, headers={"authorization": f"Bearer {token}"}, json=request_body)
        processes_dict.update({process_id: resp.json()})
    
    return processes_dict

def convert_process_statistics_dict_to_df(
        processes_dict: dict[str, Any],
        columns: list[str],
        index_name: str,
        process_rename_dict: dict[str, str]
    ) -> pd.DataFrame:
    """
    columns: list[str]
    A list of column names whose choose from common dataframe ....

    index_name: str
    Column name which set the dataframe index.

    process_rename_dict: dict[str, str]
    key -- process ID
    value -- name of process
    """
    dfs_dict = {}
    for process_id in processes_dict.keys():
        df = pd.json_normalize(processes_dict[process_id], sep='_')[columns]
        df = df.set_index(index_name)

        process_name = process_rename_dict[process_id]
        df.columns = process_name + '_' + df.columns
        
        dfs_dict.update({process_id: df})

    common_df = pd.concat(dfs_dict.values(), axis=1)
    return common_df