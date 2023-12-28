import click
import gspread
import json
from typing import Callable, Union

from sqlalchemy import create_engine
import pandas as pd

from .postprocessing import (
    get_mapping_file,
    get_param_system_object_names,
    clear_check_result,
    add_columns_to_check_result,
    get_column_order,
    get_history_tests,
    get_stats_table
)
# from db_queries import drop_duplicates_into_recent_tests
from .db_queries import get_access_to_db_tables

from .check_tests import (
    test_milestone_dates,
    test_co_production,
    test_co_sales,
    test_co_bdr
)
from .utils import generate_tokens


VERSIONS = {
    'Рабочая версия': '1ce7fe21-956f-4627-b1aa-cbfc2d6358ba',
    'Бюджет 2024. Стратегический': 'f42eb656-5747-49d0-8e4b-c26ff1c467fd',
    'Бюджет 2024. Детальный': '095212b8-169f-49a1-b5ca-64b55db7a012',
    'Бюджет 2024. Уточненный': '53c7d07c-d84c-45a5-ae4b-dfa2ff8f7059',
}

def run_test(
    test_method: Callable,
    tokens: dict[str, str],
    mapping_dict: dict[str, pd.DataFrame],
    object_names: pd.DataFrame,
    version_id: str
) -> Union[pd.DataFrame, None]:
    try:
        check_result = test_method(tokens, version_id)
        check_result = clear_check_result(check_result)
        check_result = add_columns_to_check_result(check_result, mapping_dict['col_checks'], mapping_dict['another_checks'], object_names, version_id)
        print(f'\nDONE:\tversion_id:\t{version_id}\t{test_method.__name__}')
        return check_result[get_column_order()]
    except Exception as e:
        print(f'\nFAILED:\tversion_id:\t{version_id}\t{test_method.__name__}')
        print(f'{type(e).__name__}: {e}')
        return None

def pipeline(
    tokens: dict[str, str],
    gspread_client: gspread.client.Client,
    db_conn: dict[str, str],
    save_method: Callable,
    write_params: dict
) -> None:
    """
    save_method: pd.DataFrame.to_csv or pd.DataFrame.to_sql
    """

    mapping_col_checks, mapping_another_checks, object_types = get_mapping_file(gspread_client)
    mapping_dict = {
        'col_checks': mapping_col_checks,
        'another_checks': mapping_another_checks,
        'object_types': object_types
    }
    object_names = get_param_system_object_names(mapping_dict['object_types'], tokens['parameters'], VERSIONS['Рабочая версия'])

    CALL_LIST = [
        test_milestone_dates,
        test_co_production,
        test_co_sales,
        test_co_bdr
    ]

    for version_id in VERSIONS.values():
        for test_method in CALL_LIST:
            check_result = run_test(test_method, tokens, mapping_dict, object_names, version_id)
            if check_result is not None:
                save_method(check_result, **write_params['history'])

    engine = create_engine(f"postgresql+psycopg2://{db_conn['user']}:{db_conn['password']}@{db_conn['host']}:{db_conn['port']}/{db_conn['database']}")

    for i, history_test_df in enumerate(get_history_tests(engine, mapping_dict, tokens)):
        if i > 0:
            if 'if_exists' in write_params['recent_tests'].keys():
                write_params['recent_tests'].update({'if_exists': 'append'})
            if 'mode' in write_params['recent_tests'].keys():
                write_params['recent_tests'].update({'mode': 'a', 'header': False})
        save_method(history_test_df, **write_params['recent_tests'])

    print('\nDONE: recent_tests save')

    stats_df = get_stats_table(engine, mapping_dict, tokens)
    save_method(stats_df, **write_params['stats'])
    print('\nDONE: stats_table save')

def run_save_to_db(
    creds: dict[str, dict[str, str]],
    db_conn: dict[str, str],
    gspread_client: gspread.client.Client
) -> None:
    tokens = generate_tokens(creds)

    engine = create_engine(f"postgresql+psycopg2://{db_conn['user']}:{db_conn['password']}@{db_conn['host']}:{db_conn['port']}/{db_conn['database']}")

    write_params = {
        'history': {
            'name': db_conn['table_history'],
            'con': engine,
            'schema': db_conn['schema'],
            'if_exists': 'append',
            'index': False
        },
        'recent_tests': {
            'name': db_conn['table_tests'],
            'con': engine,
            'schema': db_conn['schema'],
            'if_exists': 'replace',
            'index': False
        },
        'stats': {
            'name': db_conn['table_dash'],
            'con': engine,
            'schema': db_conn['schema'],
            'if_exists': 'replace',
            'index': False
        }
    }
    pipeline(tokens, gspread_client, db_conn, pd.DataFrame.to_sql, write_params)
    # drop_duplicates_into_recent_tests(db_conn)
    get_access_to_db_tables(db_conn)
    return None

def run_save_to_csv(
    creds: dict[str, dict[str, str]],
    db_conn: dict[str, str],
    gspread_client: gspread.client.Client
) -> None:
    tokens = generate_tokens(creds)

    now_time = pd.Timestamp.now()
    write_params = {
        'history': {
            'path_or_buf': f'checking_result {now_time}.csv',
            'mode': 'w',
            'header': True,
            'index': False,
        },
        'recent_tests':{
            'path_or_buf': f'recent_tests {now_time}.csv',
            'mode': 'w',
            'header': True,
            'index': False,
        },
        'stats': {
            'path_or_buf': f'stats_table {now_time}.csv',
            'mode': 'w',
            'header': True,
            'index': False,
        }
    }
    pd.DataFrame(columns=get_column_order()).to_csv(**write_params['history'])
    write_params['history'].update({
        'mode': 'a',
        'header': False,
    })

    pipeline(tokens, gspread_client, db_conn, pd.DataFrame.to_csv, write_params)

    return None


@click.command()
@click.option("-c", "--credentials_filename", type=click.Path(exists=True), default="credentials.json")
@click.option("-s", "--service_acc_json_file", type=click.Path(exists=True))
@click.option("-d", "--db_connection_info", type=click.Path(exists=True), default="db_connection_info.json")
def main(
    credentials_filename: str,
    service_acc_json_file: str,
    db_connection_info: str
) -> None:
    with open(credentials_filename, 'r') as f_cred:
        creds = json.load(f_cred)
    with open(db_connection_info, 'r') as f_conn:
        db_conn = json.load(f_conn)

    gspread_client = gspread.service_account(service_acc_json_file)

    run_save_to_csv(creds, db_conn, gspread_client)
    # run_save_to_db(creds, db_conn, gspread_client)


if __name__ == "__main__":
    main()
