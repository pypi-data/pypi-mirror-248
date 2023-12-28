import jwt

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