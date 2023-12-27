import re
import requests

import pandas as pd


URL_ERP_INDICATORS = 'https://erp-core.brusnika.ru/indicators/api/v2'


def get_indicator_values(
        token: str,
        version_id: str,
        indicators: list[str],
        groupby: list[str] = ["constructionObjectId"],
        filter: dict[str, list[str]]={},
    ) -> requests.Response:

    url = f'{URL_ERP_INDICATORS}/versions/{version_id}/indicator-values'
    request_body = [{
        "requestId": "",
        "indicators": indicators,
        "timeSlice": {
            "groupBy": "MONTH",
            "filter": {}
        },
        "objectSlice": {
            "groupBy": groupby,
            "filter": [filter]
        }
        }
    ]
    resp = requests.post(url, headers={"authorization": f"Bearer {token}"}, json=request_body)
    return resp

def convert_indicator_values_to_dfs_dict(
        resp: requests.Response, 
        columns: list[str]=['constructionObjectId', 'yearMonth', 'amount']
    ) -> dict[str, pd.DataFrame]:
    dfs_dict = {}
    for resp_i in resp.json():
        df = pd.DataFrame(resp_i['slices'])
        df.yearMonth = pd.to_datetime(df.yearMonth)
        indicator_name = re.sub(r'[-.]', '_', resp_i['indicator'])
        dfs_dict.update({indicator_name: df[columns]})
    return dfs_dict

def get_versions(token: str) -> pd.DataFrame:
    url = f'{URL_ERP_INDICATORS}/versions'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})
    df = pd.DataFrame(resp.json())
    return df