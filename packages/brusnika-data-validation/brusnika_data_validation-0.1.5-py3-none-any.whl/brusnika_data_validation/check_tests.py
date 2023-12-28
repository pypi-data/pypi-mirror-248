import numpy as np
import pandas as pd

from .validation import (
    Validator_co_milestone_dates,
    Validator_parcel_milestone_dates,
    Validator_co_production,
    Validator_co_bdr,
    Validator_co_bdr_standarts,
    Validator_co_sales
)


def test_milestone_dates(
    tokens: dict[str, str],
    version_id: str,
) -> pd.DataFrame:
    sdp_validator = Validator_parcel_milestone_dates(tokens)
    sdp_df = sdp_validator.get_data(version_id)
    checks_result_sdp = sdp_validator.validate(sdp_df)

    validator = Validator_co_milestone_dates(tokens)
    df, lost_obj = validator.get_data(sdp_df, version_id)
    checks_result = validator.validate(df, lost_obj)
    return pd.concat([checks_result_sdp, checks_result])

def test_co_production(
    tokens: dict[str, str],
    version_id: str
) -> pd.DataFrame:
    validator = Validator_co_production(tokens)
    df = validator.get_data(version_id)
    check_result = validator.validate(df)
    return check_result

def test_co_bdr(
    tokens: dict[str, str],
    version_id: str
) -> pd.DataFrame:
    # mapping_filepath = './validation/object_passport/budget/mapping.json'
    mapping_filepath = '/opt/airflow/dags/data-validation/validation/object_passport/budget/mapping.json'

    validator_values = Validator_co_bdr(tokens)
    df_bdr = validator_values.get_data(version_id, mapping_filepath)
    checks_result_values = validator_values.validate(df_bdr)

    validator_standarts = Validator_co_bdr_standarts(tokens)
    standarts_df = validator_standarts.get_data(df_bdr, version_id, mapping_filepath)
    checks_result_standarts = validator_standarts.validate(standarts_df)

    return pd.concat([checks_result_values, checks_result_standarts])

def test_co_sales(
    tokens: dict[str, str],
    version_id: str
) -> pd.DataFrame:
    validator = Validator_co_sales(tokens)
    df = validator.get_data(version_id)
    check_result = validator.validate(df)

    all_checks = pd.Series(validator.schema.__extras__.keys())
    notna_exist_checks = all_checks[all_checks.str.match(r'.*notna_exist.*')].tolist()
    check_result.failure_case = check_result.failure_case.replace(notna_exist_checks, np.nan)
    return check_result

# CALL_LIST = [
#     test_milestone_dates,
#     test_co_production,
#     test_co_sales,
#     test_co_bdr
# ]
