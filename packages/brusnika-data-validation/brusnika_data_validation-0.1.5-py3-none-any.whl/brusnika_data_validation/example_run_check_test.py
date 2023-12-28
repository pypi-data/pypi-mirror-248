import jwt
from .validation import Validator_perm_start_comm_dates


def main(
    param_token: str,
    process_token: str,
    indicator_token: str,
    version_token: str
) -> None:

    validator = Validator_perm_start_comm_dates()
    df, lost_obj = validator.get_data(param_token, process_token, indicator_token, version_token)

    checks_result = validator.validate(df, lost_obj)
    # checks_result.to_csv('test_permission_const_start_commition_dates_result.csv', index=False)


if __name__ == "__main__":
    iss = ""
    key = ""
    key_v = ""

    aud = "erp-core.brusnika.ru/parameters"
    param_token = jwt.encode({"iss": iss, "aud": aud}, key)

    aud = "erp-core.brusnika.ru/processes"
    process_token = jwt.encode({"iss": iss, "aud": aud}, key)

    aud = "erp-core.brusnika.ru/indicators"
    indicator_token = jwt.encode({"iss": iss, "aud": aud}, key)

    aud = "erp-core.brusnika.ru/versioning"
    version_token = jwt.encode({"iss": iss, "aud": aud}, key_v)

    main(param_token, process_token, indicator_token, version_token)
