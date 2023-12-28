from ast import literal_eval
import gspread
import requests
from typing import Union, Optional

import numpy as np
import pandas as pd
import sqlalchemy

from .db_queries import get_test_dfs_from_db, get_queries_unique_test, get_query_history_records
from .utils import parameters, versioning


def _divide_df_by_schema_context(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_col = df[df['schema_context'] == 'Column'].copy(deep=True)
    df_another = df[df['schema_context'] != 'Column'].copy(deep=True)
    return df_col, df_another

def _get_cols_to_group(is_column_check: bool=False) -> tuple[list[str], str]:
    """Return column names to group or to set index,
    and one column name to drop from set.
    """
    cols_to_group = ['test_name', 'schema_context', 'check_name']
    add_or_drop_col_name = ('column_name', 'threshold')
    if is_column_check:
        cols_to_group.append('column_name')
    else:
        cols_to_group.append('threshold')
    return cols_to_group, (set(add_or_drop_col_name) - set(cols_to_group)).pop()

def _get_failure_count(df: pd.DataFrame, is_column_check: bool):
    """Calculate failure counts for one check."""
    cols_to_group, _ = _get_cols_to_group(is_column_check)
    failure_counts = df.groupby(by=cols_to_group).object_index.count()
    failure_counts.name = 'failure_count'
    return failure_counts

def _get_mapping_key(df: pd.DataFrame, is_column_check: bool):
    """Concatenation indexed columns into one."""
    cols, _ = _get_cols_to_group(is_column_check)
    mapping_key = df[cols].drop_duplicates()
    mapping_key['mapping_key'] = mapping_key.apply(lambda x: '_'.join(x.tolist()), axis=1)
    mapping_key = mapping_key.set_index(cols).mapping_key
    return mapping_key

def _add_data_to_dataframe(df: pd.DataFrame, add_data: Union[pd.Series, pd.DataFrame]):
    return df.merge(add_data, how='left', left_on=add_data.index.names, right_index=True)

def add_columns_by_schema_context(df: pd.DataFrame, mapping: pd.DataFrame, is_column_check: bool):
    """Add information into dataframe containing specific schema context.

    Columns to be added:
    failure_count, data_source, object_type, failure_case_unit
    """
    failure_count = _get_failure_count(df, is_column_check)
    result_df = _add_data_to_dataframe(df, failure_count)
    result_df = _add_data_to_dataframe(result_df, mapping.drop(columns='rus_description'))
    mapping_key = _get_mapping_key(result_df, is_column_check)
    result_df = _add_data_to_dataframe(result_df, mapping_key)
    return result_df

def add_columns_to_check_result(
    checks_result: pd.DataFrame,
    mapping_col_checks: pd.DataFrame,
    mapping_another_checks: pd.DataFrame,
    object_names_df: pd.DataFrame,
    version_id: str,
    comparison_version_id: Optional[str]=None
):
    """Add information into one check result.

    Information to be added:
    failure count, mapping information (without russian description), object names and version ids.

    version_id: str
    ID of version for which to run checks
    comparison_version_id: str
    ID of second version (if checks are run between versions)
    """
    result_df = checks_result.copy(deep=True)
    result_df.failure_case = pd.to_numeric(result_df.failure_case)
    result_df.threshold = result_df.threshold.replace(np.nan, '')
    result_df.threshold = result_df.threshold.astype('str')

    col_checks, another_checks = _divide_df_by_schema_context(result_df)
    if not col_checks.empty:
        col_checks = add_columns_by_schema_context(col_checks, mapping_col_checks, is_column_check=True)
    if not another_checks.empty:
        another_checks = add_columns_by_schema_context(another_checks, mapping_another_checks, is_column_check=False)

    result_df = pd.concat([col_checks, another_checks])
    result_df = _add_data_to_dataframe(result_df, object_names_df)
    result_df['version_id'] = version_id
    result_df['comparison_version_id'] = comparison_version_id
    return result_df

def clear_check_result(df: pd.DataFrame) -> pd.DataFrame:
    """Choose failure cases that are equal to the difference
    between the compared values for DataFrameSchema check
    and column value for Column check.
    """
    mask_dataframe_check = (df['schema_context'] == "DataFrameSchema")
    df_checks = df[mask_dataframe_check].copy(deep=True)

    df_lost_cols = (
        df_checks[df_checks['check_name'] == 'column_in_dataframe']
        .drop(columns='column_name')
        .rename(columns={'failure_case': 'column_name'})
    )
    df_lost_cols['schema_context'] = 'Column'

    df_checks = df_checks[df_checks.apply(lambda x: x['check_name'] == x['column_name'], axis=1)]

    clear_df = pd.concat([df[~mask_dataframe_check], df_checks, df_lost_cols])
    del mask_dataframe_check, df_checks
    return clear_df

def get_unique_object_types(object_type: pd.Series) -> list[str]:
    tuples_mask = object_type.str.match(r'\(.*\)')

    tuples_explode_series = object_type[tuples_mask].apply(literal_eval).explode()

    tuples_explode_list = tuples_explode_series[~tuples_explode_series.str.startswith("_")].unique()
    single_types = object_type[~tuples_mask].unique()

    del tuples_mask, tuples_explode_series
    return list(set(tuples_explode_list) | set(single_types))

def get_mapping_file(gspread_client: gspread.client.Client) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Return 2 datasets of mapping:
    first for column checks (schema_context: Column),
    second for another checks (schema_context: DataFrameSchema or custom type (e.g. InputData)),

    and object types series from mapping.
    """
    file_id = "1sNPuLInRHpRWGwTRn7LrGynrssSYGZgFZFOrPyc3tsA"
    spreadsheet = gspread_client.open_by_key(file_id)

    mapping = pd.DataFrame(spreadsheet.get_worksheet_by_id(0).get_values(combine_merged_cells=True))
    mapping.columns = mapping.iloc[0]
    mapping = mapping.drop(index=0)

    def _set_index_and_drop_column(df, is_column_check):
        index_cols, drop_col = _get_cols_to_group(is_column_check)
        result_df = df.set_index(index_cols)
        result_df = result_df.drop(columns=drop_col)
        return result_df

    mapping_col_checks, mapping_another_checks = _divide_df_by_schema_context(mapping)
    mapping_col_checks = _set_index_and_drop_column(mapping_col_checks, is_column_check=True)
    mapping_another_checks = _set_index_and_drop_column(mapping_another_checks, is_column_check=False)
    return mapping_col_checks, mapping_another_checks, get_unique_object_types(mapping.object_type)

def get_param_system_object_names(object_types: list, param_token: str, version_id: str) -> pd.DataFrame:
    """Return dataset with all object names from parametric system for object types."""
    obj_name_dfs = []
    for obj_type in object_types:
        if obj_type == "":
            raise ValueError("Object type has empty string value.")

        if obj_type == 'construction-objects':
            obj_name_df = parameters.get_construction_objects(param_token, version_id)
            obj_name_df = obj_name_df.reset_index()
        else:
            url = f'https://erp-core.brusnika.ru/parameters/v1/versions/{version_id}/{obj_type}'
            resp = requests.get(url, headers={"authorization": f"Bearer {param_token}"})
            if resp.status_code in [400, 404]:
                raise ValueError(f"Object type not found in parametric system: {obj_type}")
            obj_name_df = pd.json_normalize(resp.json(), sep='_')

        obj_name_df = obj_name_df[['id', 'fullName']]
        obj_name_df = obj_name_df.rename(columns={'id': 'object_index', 'fullName': 'object_name'})
        obj_name_df['object_type'] = obj_type
        obj_name_dfs.append(obj_name_df)

    return pd.concat(obj_name_dfs).set_index(['object_type', 'object_index'])

def get_column_order() -> list[str]:
    columns = [
        'datetime',
        'version_id',
        'comparison_version_id',
        'mapping_key',
        'test_name',
        'schema_context',
        'check_name',
        'column_name',
        'threshold',
        'obj_count',
        'failure_count',
        'failure_case',
        'failure_case_unit',
        'object_index',
        'object_type',
        'object_name',
        'data_source'
    ]
    return columns

def get_column_order_rename_table() -> list[str]:
    columns = get_column_order()
    columns.insert(0, 'test_type')
    columns.insert(columns.index('test_name'), 'rus_description')
    columns.insert(columns.index('version_id')+1, 'version_name')
    columns.extend(['department', 'responsible'])

    drop_names = ['schema_context', 'check_name', 'column_name']
    for col_name in drop_names:
        columns.remove(col_name)
    return columns

def get_history_tests(
    engine: sqlalchemy.engine.base.Engine,
    mapping_dict: dict[str, pd.DataFrame],
    tokens: dict[str, str]
) -> pd.DataFrame:
    queries_dict = get_queries_unique_test()
    for test_type, query in queries_dict.items():
        df = pd.read_sql(get_query_history_records(query), engine)
        df['test_type'] = test_type

        col_checks, another_checks = _divide_df_by_schema_context(df)
        col_checks = _add_data_to_dataframe(col_checks, mapping_dict['col_checks'][['rus_description', 'department', 'responsible']])
        another_checks = _add_data_to_dataframe(another_checks, mapping_dict['another_checks'][['rus_description', 'department', 'responsible']])
        result_df = pd.concat([col_checks, another_checks])

        version_names = versioning.get_version_names(tokens['versioning'])
        result_df = _add_data_to_dataframe(result_df, version_names)
        yield result_df[get_column_order_rename_table()]

def _calc_failure_percent(df) -> pd.Series:
    return df.failure_count / df.obj_count

def get_mapping_for_stats(mapping_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
    mapping_col_checks = mapping_dict['col_checks'].reset_index()
    mapping_key = _get_mapping_key(mapping_col_checks, is_column_check=True)
    mapping_col_checks = _add_data_to_dataframe(mapping_col_checks, mapping_key)

    mapping_another_checks = mapping_dict['another_checks'].reset_index()
    mapping_key = _get_mapping_key(mapping_another_checks, is_column_check=False)
    mapping_another_checks = _add_data_to_dataframe(mapping_another_checks, mapping_key)

    mapping = pd.concat([mapping_col_checks, mapping_another_checks], axis=0)

    columns = [
        'test_name',
        'mapping_key',
        'rus_description',
        'threshold',
        'failure_case_unit',
        'data_source',
        'department',
        'responsible'
    ]
    mapping = mapping[columns]
    mapping = mapping.set_index('mapping_key')
    mapping.threshold = mapping.threshold.replace(np.nan, '')
    mapping.threshold = mapping.threshold.astype('str')

    del mapping_col_checks, mapping_another_checks, columns
    return mapping

def get_stats_table(
    engine: sqlalchemy.engine.base.Engine,
    mapping_dict: dict[str, pd.DataFrame],
    tokens: dict[str, str]
) -> pd.DataFrame:
    test_dfs = get_test_dfs_from_db(engine)

    index_cols = ['version_id', 'mapping_key']
    for table_name, df in test_dfs.items():
        df['percent'] = _calc_failure_percent(df)
        df = df.sort_values(by=index_cols).set_index(index_cols)
        df.columns = table_name + '_' + df.columns
        test_dfs.update({table_name: df})

    stats_df = pd.concat(test_dfs.values(), axis=1)
    stats_df = stats_df.reset_index()

    common_mapping = get_mapping_for_stats(mapping_dict)
    stats_df = _add_data_to_dataframe(stats_df, common_mapping)

    version_names = versioning.get_version_names(tokens['versioning'])
    stats_df = _add_data_to_dataframe(stats_df, version_names)

    is_na_rus_description = stats_df.rus_description.replace('', None).isna()
    if is_na_rus_description.any():
        lost_naming = stats_df[is_na_rus_description].mapping_key.unique()
        print(f"WARNING: Russian description of checks is absent:")
        for mapping_key in lost_naming:
            print(f'\t{mapping_key}')

    columns = ['version_id', 'version_name', 'test_name', 'mapping_key', 'rus_description', 'threshold',  'failure_case_unit']
    columns += stats_df.columns[~stats_df.columns.isin(columns)].tolist()

    del test_dfs, index_cols, common_mapping
    return stats_df[columns]
