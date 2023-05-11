from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

import pandas


class BaseExcelConverter(ABC):
    @abstractmethod
    def convert_excel_to_pandas_dataframe(
        self, excel_file: Path | str | BinaryIO
    ) -> pandas.DataFrame:
        raise NotImplementedError
