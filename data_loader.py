import pandas as pd
from pandera.typing import DataFrame
import pandera as pa
from schemas import OnlineDataSchema, OfflineDataSchema


class DataLoader:
    def __init__(self, path: str) -> None:
        self.path = path

    @pa.check_types(lazy=True)
    def load_online_data(
        self, sheet_name: str, engine: str = "openpyxl"
    ) -> DataFrame[OnlineDataSchema]:
        df = pd.read_excel(self.path, sheet_name=sheet_name, engine=engine)
        return df

    @pa.check_types(lazy=True)
    def load_offline_data(
        self, sheet_name: str, engine: str = "openpyxl"
    ) -> DataFrame[OfflineDataSchema]:
        df = pd.read_excel(self.path, sheet_name=sheet_name, engine=engine)
        return df
