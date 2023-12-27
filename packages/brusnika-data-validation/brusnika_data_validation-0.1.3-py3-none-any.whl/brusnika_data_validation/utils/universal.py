import sys
from typing import Callable, Optional

import numpy as np
import pandas as pd


def compare_diff_with_threshold(diff: pd.Series, compare_func: Callable=pd.Series.eq, threshold: float=0., exclude_na: bool=True) -> pd.Series:
    """Сompare float series with a threshold value.

    compare_func: pd.Series.eq, pd.Series.gt, pd.Series.ge, pd.Series.lt or pd.Series.le (by default pd.Series.eq)
        eq - Equal to
        gt - Greater than
        ge - Greater than or equal
        lt - Less than
        le - Less than or equal
        
    threshold: float, treshold value 
    exclude_na: bool=True
    exclude empty values from result for NaN values, the checking result equal to True, if exclude_na=True
    """
    result = compare_func(diff, threshold)
    if exclude_na:
        na_indexes = diff.isna()
        return result | na_indexes
    return result

def get_abs_diff(first_value: pd.Series, second_value: pd.Series) -> pd.Series:
    return np.abs(second_value - first_value)

def get_abs_diff_fillna(first_value: pd.Series, second_value: pd.Series, fill_value: float) -> pd.Series:
    return np.abs(second_value.sub(first_value, fill_value=fill_value))

def get_relative_diff(first_value: pd.Series, second_value: pd.Series) -> pd.Series:
    return get_abs_diff(first_value, second_value) / second_value

def get_diff_days(first_date: pd.Series, second_date: pd.Series) -> pd.Series:
    """Return count of days between two dates (int or nan)
    
    first_date, second_date: pd.Series, value type is datetime
    """
    diff = second_date - first_date
    return diff.dt.days

def get_diff_month(first_date: pd.Series, second_date: pd.Series):
    """ Calc diff between month start of two dates.
    Сalculation error no more than 1 month.
    Return count of month between two dates (int or nan)

    first_date, second_date: pd.Series, value type is datetime
    """
    diff = second_date.dt.to_period('M') - first_date.dt.to_period('M')
    diff = diff.apply(lambda x: x.n if not pd.isna(x) else np.nan)
    return diff

def set_diff(df: pd.DataFrame, diff: pd.Series, col_name: Optional[str]=None) -> None:
    if col_name is None:
        col_name = sys._getframe(1).f_code.co_name
    df[col_name] = diff

def calc_sum_cols(df: pd.DataFrame, term_cols: list[str], min_count: int = 1) -> pd.Series:
    """
    Calculate dataframe columns sum (axis=1)
    
    min_count : int, default 0
    The required number of valid values to perform the operation. If fewer than
    ``min_count`` non-NA values are present the result will be NA.
    """
    return df[term_cols].sum(axis=1, min_count=min_count)
    
