import requests
import pandas as pd


URL_ERP_VERSIONING = 'https://scheduler.brusnika.ru/backend/versioning/v2'


def get_versions(token: str) -> pd.DataFrame:
    url = f'{URL_ERP_VERSIONING}/versions'
    resp = requests.get(url, headers={"authorization":f"Bearer {token}"})
    df = pd.json_normalize(resp.json(), sep="_")
    df = df.set_index('id')
    return df

def get_version_names(token: str) -> pd.Series:
    df = get_versions(token)
    df = df.rename(columns={'title': 'version_name'})
    df.index.name = 'version_id'
    return df['version_name']

def get_release_version(token: str, versions_list: list[str]) -> str:
    """
    versions_list: list[str]
    A list of version IDs from needed system

    Return last approved version ID
    """
    df = get_versions(token)[['title', 'state', 'createdAt']]
    
    df_version = df.loc[versions_list]
    df_version.createdAt = pd.to_datetime(df_version.createdAt.str.split('T', expand=True).iloc[:, 0])
    df_version = df_version[df_version.state == 'APPROVED'].sort_values('createdAt')
    last_approved_version = df_version.iloc[-1].name
    
    return last_approved_version