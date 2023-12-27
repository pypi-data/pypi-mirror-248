import requests
import pandas as pd


URL_ERP_VERSIONING = 'https://scheduler.brusnika.ru/backend/versioning/v2'


def get_release_version(token: str, versions_list: list[str]) -> str:
    """
    versions_list: list[str]
    A list of version IDs from needed system

    Return last approved version ID
    """
    url = f'{URL_ERP_VERSIONING}/versions'
    resp = requests.get(url, headers={"authorization":f"Bearer {token}"})
    df = pd.DataFrame(resp.json())
    df = df.set_index('id')[['title', 'state', 'createdAt']]
    
    df_version = df.loc[versions_list]
    df_version.createdAt = pd.to_datetime(df_version.createdAt.str.split('T', expand=True).iloc[:, 0])
    df_version = df_version[df_version.state == 'APPROVED'].sort_values('createdAt')
    last_approved_version = df_version.iloc[-1].name
    
    return last_approved_version