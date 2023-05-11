import random

from datetime import datetime
from calendar import monthrange
from pathlib import Path
from typing import BinaryIO

import pandas

from src.services.excel_converter.base import BaseExcelConverter


class TestDataExcelConverter(BaseExcelConverter):
    id_name = ("id", "Unnamed: 0_level_1", "Unnamed: 0_level_2")
    company_name = ("company", "Unnamed: 1_level_1", "Unnamed: 1_level_2")
    date_name = "date"

    def convert_excel_to_pandas_dataframe(
        self, excel_file: Path | str | BinaryIO
    ) -> pandas.DataFrame:
        data = pandas.read_excel(excel_file, header=[0, 1, 2])
        data = self._add_dates(data, 2023, 12)
        data = self._unpivot_data_frame(data)
        return data

    def _unpivot_data_frame(self, data: pandas.DataFrame) -> pandas.DataFrame:
        data = data.melt(
            id_vars=[
                self.id_name,
                self.company_name,
                self.date_name,
            ],
            value_vars=[
                ("fact", "Qliq", "data1"),
                ("fact", "Qliq", "data2"),
                ("fact", "Qoil", "data1"),
                ("fact", "Qoil", "data2"),
                ("forecast", "Qliq", "data1"),
                ("forecast", "Qliq", "data2"),
                ("forecast", "Qoil", "data1"),
                ("forecast", "Qoil", "data2"),
            ],
            var_name=["plan_fact", "q_type", "data_type"],  # type: ignore
        )
        data = data.rename(columns={self.company_name: "company"})
        return data

    def _add_dates(
        self, data: pandas.DataFrame, year: int, month: int
    ) -> pandas.DataFrame:
        date = [
            datetime(year, month, random.randint(*monthrange(year, month)))
            for _ in data.index
        ]
        data[self.date_name] = date
        return data
