import pandas as pd


def get_not_canceled_objects(df: pd.DataFrame, return_index: bool = True) -> pd.Index:
    """Return list of not cancelled objects id."""
    if return_index:
        return df.index[~df.canceled]
    return df[~df.canceled]