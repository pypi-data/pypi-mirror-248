import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import Error
import sqlalchemy


def get_query_edge_tests(is_recent: bool) -> str:
    order_by = ""
    if is_recent:
        order_by = "desc"
    query = f"""
    select distinct on (version_id, mapping_key) version_id, mapping_key, datetime,  obj_count, failure_count
    FROM data_validation.history
    order by version_id, mapping_key, datetime {order_by}
    """
    return query

def get_query_previous_tests() -> str:
    query = """
    select version_id, mapping_key, datetime, obj_count, failure_count
    from
    (
    	select distinct version_id, mapping_key, datetime, obj_count, failure_count,
    		row_number() over(partition by version_id, mapping_key order by datetime desc) as serial_number
    	FROM data_validation.history
    	group by version_id, mapping_key, datetime, obj_count, failure_count
    ) as numbered
    where numbered.serial_number = 2
    """
    return query

def get_query_start_month_tests(query_unique_tests: str) -> str:
    """
    query_unique_tests: str
    Query of unique tests from which the beginning of the month will be searched.
    """
    query = f"""
    select distinct on (all_tests.version_id, all_tests.mapping_key) 
    	all_tests.version_id, all_tests.mapping_key, all_tests.datetime, all_tests.obj_count, all_tests.failure_count
    from ({query_unique_tests}) as unique_tests
    left join (
    	select distinct version_id, mapping_key, datetime, obj_count, failure_count
    	FROM data_validation.history
    	group by version_id, mapping_key, datetime, obj_count, failure_count
    	order by version_id, mapping_key, datetime desc
    ) as all_tests
    on unique_tests.version_id = all_tests.version_id and 
    	unique_tests.mapping_key = all_tests.mapping_key and
    	extract (month from unique_tests.datetime) = extract (month from all_tests.datetime) and
    	extract (year from unique_tests.datetime) = extract (year from all_tests.datetime)
    order by all_tests.version_id, all_tests.mapping_key, all_tests.datetime
    """
    return query

def get_queries_unique_test() -> dict[str, str]:
    query_previous_tests = get_query_previous_tests()
    queries_dict = {
        "recent": get_query_edge_tests(is_recent=True),
        "previous": query_previous_tests,
        "start_month": get_query_start_month_tests(query_previous_tests),
        "first": get_query_edge_tests(is_recent=False),
    }
    return queries_dict

def get_test_dfs_from_db(engine: sqlalchemy.engine.base.Engine) -> dict[str, pd.DataFrame]:
    queries_dict = get_queries_unique_test()
    tests_dfs = {}
    for test_name, query in queries_dict.items():
        df = pd.read_sql(query, engine)
        tests_dfs.update({test_name: df})
    return tests_dfs

def get_query_history_records(test_query: str) -> str:
    """
    test_query: str
    Query of unique tests (recent, previous, start of month or first)
    """
    query = f"""
    select history.*
    from ({test_query}) as unique_tests
    left join data_validation.history as history
    on unique_tests.version_id = history.version_id and 
    	unique_tests.mapping_key = history.mapping_key and
    	unique_tests.datetime = history.datetime
    """
    return query

def open_access_to_table(cursor: psycopg2.extensions.cursor, table_name: str) -> None:
    cursor.execute(f"""
    GRANT UPDATE, REFERENCES, TRUNCATE, SELECT, DELETE, INSERT, TRIGGER 
    ON TABLE {table_name} TO superset_lake
    """)

# def drop_duplicates_into_recent_tests(db_conn: dict[str, str]) -> None:
def get_access_to_db_tables(db_conn: dict[str, str]) -> None:
    connection = psycopg2.connect(user=db_conn['user'],
                              password=db_conn['password'],
                              host=db_conn['host'],
                              port=db_conn['port'],
                              database=db_conn['database'])
    cursor = connection.cursor()

    #### drop_duplicates_into_recent_tests
    # table_name = f"{db_conn['schema']}.{db_conn['table_tests']}"
    # cursor.execute(f"CREATE TABLE {table_name}_temp (LIKE {table_name});")
    # cursor.execute(f"""
    # INSERT INTO {table_name}_temp
    # SELECT DISTINCT ON (datetime, version_id, mapping_key, object_index) *
    # FROM {table_name};
    # """)
    # cursor.execute(f"DROP TABLE {table_name};")
    # cursor.execute(f"""
    # ALTER TABLE {table_name}_temp
    # RENAME TO {db_conn['table_tests']};
    # """)
    open_access_to_table(cursor, f"{db_conn['schema']}.{db_conn['table_tests']}")
    open_access_to_table(cursor, f"{db_conn['schema']}.{db_conn['table_dash']}")
    connection.commit()
    cursor.close()
    connection.close()
    return None