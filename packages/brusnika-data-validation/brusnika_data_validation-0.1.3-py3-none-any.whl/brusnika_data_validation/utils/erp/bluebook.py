import re
import requests

import pandas as pd
import xmltodict


URL_ERP_BLUEBOOK = 'https://bluebook.brusnika.ru/api/v1/standards'


def get_standard_cost(token: str) -> pd.DataFrame:
    url = f'{URL_ERP_BLUEBOOK}/standard_cost/value'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})
    standard_json = xmltodict.parse(resp.text)['financial-standard']
    
    standart_dfs = {}
    for key in standard_json.keys():
        if re.match(r'\W', key) is None:
            df = pd.DataFrame.from_dict(standard_json[key], orient='columns')
            df = df.astype('float')
            standart_dfs.update({key: df})
    del df
    standarts_df = pd.concat(standart_dfs)
    
    return standarts_df