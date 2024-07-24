import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
from schemas import OnlineDataSchema, OfflineDataSchema


@pa.check_types(lazy=True)
def load_online_data(
    path: str, sheet_name: str, engine: str = "openpyxl"
) -> DataFrame[OnlineDataSchema]:
    df = pd.read_excel(fn, sheet_name=sheet_name, engine=engine)
    return df


path = r"C:\Projects\bioreactor_volume\data\meassurements.xlsx"

df = load_online_data(path, sheet_name="online")
print(df.head())
