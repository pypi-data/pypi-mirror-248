import json
import re
import requests

import numpy as np
import pandas as pd

URL_ERP_PARAMETERS = 'https://erp-core.brusnika.ru/parameters/v1'


def get_construction_objects(
        token: str,
        version_id: str,
        *,
        all: bool = True,
        construction: bool = False,
        infrastructure: bool = False,
        transient: bool = False
    ) -> pd.DataFrame:
    """Return dataset of all construction objects from parametric system by default (all=True).
    If you don`t need all objects, all=False and select the desired types of objects: construction, infrastructure, transient.
    """
    obj_urls = [
        'construction-objects',
        'infrastructure-objects',
        'transient-objects'
    ]
    if not all:
        obj_urls = np.array(obj_urls)[[construction, infrastructure, transient]]
    
    objects_list = []
    for obj_url in obj_urls:
        url = f'{URL_ERP_PARAMETERS}/versions/{version_id}/{obj_url}'
        resp = requests.get(url, headers={"authorization": f"Bearer {token}"})
        objects_list.extend(resp.json())
    
    df = pd.json_normalize(objects_list, sep='_')
    df = df.set_index('id')

    del url, resp, objects_list, obj_urls
    return df

def get_parcels(token: str, version_id: str) -> pd.DataFrame:
    url = f'{URL_ERP_PARAMETERS}/versions/{version_id}/parcels'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})

    df = pd.json_normalize(resp.json(), sep='_')
    df = df.set_index('id')

    del url, resp
    return df

def get_sites(token: str, version_id: str) -> pd.DataFrame:
    url = f'{URL_ERP_PARAMETERS}/versions/{version_id}/sites'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})

    df = pd.json_normalize(resp.json(), sep='_')
    df = df.set_index('id')

    del url, resp
    return df

def get_construction_projects(token: str, version_id: str) -> pd.DataFrame:
    url = f'{URL_ERP_PARAMETERS}/versions/{version_id}/construction-projects'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})

    df = pd.json_normalize(resp.json(), sep='_')
    df = df.set_index('id')

    del url, resp
    return df

def get_contours(token: str) -> pd.DataFrame:
    """Return dataset of contours from parametric system.
    
    Index name: 'contour_id'
    Columns: 'contour_code', 'contour_name'
    """
    url = f'{URL_ERP_PARAMETERS}/contours'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})

    df = pd.DataFrame(resp.json())
    df = df[['id', 'code', 'fullName']]
    df = df.rename(columns={
        'code': 'contour_code',
        'fullName': 'contour_name',
        'id': 'contour_id'
    })
    df = df.set_index('contour_id')
    return df


def get_grades(token: str) -> pd.DataFrame:
    """Return dataset of grades from parametric system.
    
    Index name: 'grade_id'
    Columns: 'grade' (letter code)
    """
    url = f'{URL_ERP_PARAMETERS}/grades'
    resp = requests.get(url, headers={"authorization": f"Bearer {token}"})
    
    df = pd.DataFrame(resp.json())
    df = df.rename(columns={'letter': 'grade', 'id': 'grade_id'})
    df = df.set_index('grade_id')
    return df

def get_financial_data_root_items(token: str, version_id: str, root_items: list[str]=[]) -> pd.DataFrame:
    request_body = {
        "objectFilter": [{
            "rootItems": root_items,
        }],
        "groupBy": [
            "CONSTRUCTION_OBJECT",
            "ROOT_ITEMS"
        ]
    }
    url = f'{URL_ERP_PARAMETERS}/versions/{version_id}/financial-statistics'
    resp = requests.post(url, headers={"authorization": f"Bearer {token}"}, json=request_body)

    df = pd.json_normalize(resp.json(), record_path='items', sep='_', meta=[['constructionObject', 'id']])
    result_df = pd.pivot_table(df, values='amount', index='constructionObject_id', columns='rootItem_key', aggfunc=np.sum)
    result_df.columns.name = None
    result_df.index.name = 'constructionObject'
    result_df = result_df.rename(columns=result_df.columns.to_series().apply(lambda x: re.sub(r'[-.]', '_', x)))

    del df
    return result_df

def get_area_statistics_sfa(token: str, version_id: str, groupby: list[str] = ["CONSTRUCTION_OBJECT"]) -> pd.DataFrame:
    request_body = {
      "objectFilter": [{
          "commonSpace": [False],
          "lost": [False],
          "premiseKind": [
              "RESIDENTIAL",
              "COMMERCIAL",
              "PARKING",
              "STORAGE",
          ]
      }],
      "groupBy": groupby
    }

    url = f'https://erp-core.brusnika.ru/parameters/v1/versions/{version_id}/area-statistics'
    resp = requests.post(url, headers={"authorization":f"Bearer {token}"}, json=request_body)

    df = pd.json_normalize(resp.json(), sep='_')
    return df