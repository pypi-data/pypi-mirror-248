from abc import ABC, abstractmethod
import pandas as pd
import pandera as pa
import pandera.extensions as extensions
from typing import Optional, Union, Callable


class Validator(ABC):
    def __init__(
        self,
        schema: Optional[pa.DataFrameModel],
        tokens: dict[str, str]
    ) -> None:
        self.schema = schema
        self.tokens = tokens

    def _add_check_to_schema(self, check_name: str, check_args: Union[dict, tuple]=()) -> None:
        self.schema.__extras__.update({check_name: check_args})

    def _create_check(self, factory_method: Callable[[str, float], Callable], factory_args: dict, check_name: str) -> str:
        check = factory_method(**factory_args) 
        check.__name__ = check_name
        extensions.register_check_method(check)
        return check.__name__
    
    def _generate_checks(self) -> None:
        pass

    def _get_threshold(self) -> pd.Series:
        """Return series with thresholds of checks.
        index: check name
        value: threshold (float)
        """
        threshold_dict = {}
        for check_name, check_params in self.schema.__extras__.items():
            if isinstance(check_params, dict):
                threshold_dict.update({check_name: check_params.get('threshold')})
        threshold_series = pd.Series(threshold_dict)
        threshold_series.name = 'threshold'
        return threshold_series
            
    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        raise NotImplementedError("Invalid concrete implementation of Validator")

    def validate(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        try:
            self.schema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as error:
            result_df = error.failure_cases
            result_df = result_df.rename(columns={
                "check": "check_name",
                "column": "column_name",
                "index": "object_index", 
            })
            threshold_values = self._get_threshold()
            threshold_column = result_df.merge(threshold_values, how='left', left_on='check_name', right_index=True).threshold
            result_df.insert(result_df.columns.get_loc('check_name') + 1, column='threshold', value=threshold_column)
            
            result_df = result_df.drop(columns='check_number')
            return result_df
        return None


 
