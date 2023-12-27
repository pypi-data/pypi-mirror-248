import json
import jwt
import re
import requests
import pandas as pd


def get_token(creds: dict, system_name: str):
    if creds.get(system_name):
        iss = creds[system_name]['iss']
        aud = creds[system_name]['aud']
        key = creds[system_name]['key']
        return jwt.encode({"iss": iss, "aud": aud}, key)
    return None

def generate_tokens(creds: dict[str, dict[str, str]]) -> dict[str, str]:
    tokens = {}
    for system in creds.keys():
        tokens.update({system: get_token(creds, system)})
    return tokens

def get_version_names(token: str) -> pd.Series:
    url = 'https://scheduler.brusnika.ru/backend/versioning/v2/versions'
    resp = requests.get(url, headers={"authorization":f"Bearer {token}"})
    df = pd.DataFrame(resp.json())
    df = df.rename(columns={'id': 'version_id', 'title': 'version_name'})
    version_names = df.set_index('version_id').version_name
    return version_names

def get_not_canceled_objects(df: pd.DataFrame, return_index: bool = True) -> pd.Index:
    """Return list of not cancelled objects id."""
    if return_index:
        return df.index[~df.canceled]
    return df[~df.canceled]