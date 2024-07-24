import pandas as pd
from pandera.typing import DataFrame
import pandera as pa
from schemas import OnlineDataSchema, OfflineDataSchema


@pa.check_types(lazy=True)
def load_online_data(
    path: str, sheet_name: str, engine: str = "openpyxl"
) -> DataFrame[OnlineDataSchema]:
    df = pd.read_excel(path, sheet_name=sheet_name, engine=engine)
    return df


@pa.check_types(lazy=True)
def load_offline_data(
    path: str, sheet_name: str, engine: str = "openpyxl"
) -> DataFrame[OfflineDataSchema]:
    df = pd.read_excel(path, sheet_name=sheet_name, engine=engine)
    return df
