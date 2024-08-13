import pandas as pd
import pandera as pa
from pandera import DataFrameModel
from pandera.typing import Series


class OnlineDataSchema(DataFrameModel):
    """Schema for online data"""

    time_h: Series[float] = pa.Field(ge=0, coerce=True)
    acid_total_ml: Series[float] = pa.Field(ge=0, coerce=True)
    base_total_ml: Series[float] = pa.Field(ge=0, coerce=True)
    antifoam_total_ml: Series[float] = pa.Field(ge=0, coerce=True)
    stream_1_total_ml: Series[float] = pa.Field(ge=0, coerce=True)
    stream_2_total_ml: Series[float] = pa.Field(ge=0, coerce=True)

    @pa.dataframe_check()
    def check_cum_sum(cls, df: pd.DataFrame) -> bool:
        # Check if the cumulative sum of each column is not zero
        columns_with_zero_cumsum = [
            col for col in df.columns if df[col].cumsum().iloc[-1] == 0
        ]
        if columns_with_zero_cumsum:
            raise pa.errors.SchemaError(
                schema=cls,
                data=df,
                message=f"Columns with zero cumulative sum: {columns_with_zero_cumsum}",
            )
        return True


class SampleSchema(DataFrameModel):
    """Schema for offline data"""

    t_sample_h: Series[float] = pa.Field(ge=0, coerce=True)
    v_sample_ml: Series[float] = pa.Field(le=0, coerce=True)
