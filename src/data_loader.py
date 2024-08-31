import pandas as pd
from pandera.typing import DataFrame
import pandera as pa
from src.schemas import AdditionDataSchema, SampleSchema


class DataLoader:
    def __init__(self, path: str) -> None:
        self.path = path

    @pa.check_types(lazy=True)
    def load_addition_data(
        self, sheet_name: str, engine: str = "openpyxl"
    ) -> DataFrame[AdditionDataSchema]:
        df = pd.read_excel(self.path, sheet_name=sheet_name, engine=engine)
        return df

    @pa.check_types(lazy=True)
    def load_sample_data(
        self, sheet_name: str, engine: str = "openpyxl"
    ) -> DataFrame[SampleSchema]:
        df = pd.read_excel(self.path, sheet_name=sheet_name, engine=engine)
        return df
