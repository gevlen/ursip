import typing

import pandas

from src.services.excel_converter.base import BaseExcelConverter

excel_extensions = (
    ".xlsx",
    ".xlsm",
    ".xlsb",
    ".xltx",
    ".xltm",
    ".xls",
    ".xlt",
    ".xml",
)


def get_pandas_data_frame(
    excel_file: typing.BinaryIO, converter: BaseExcelConverter
) -> pandas.DataFrame | None:
    try:
        data = converter.convert_excel_to_pandas_dataframe(excel_file=excel_file)
        return data
    except KeyError:
        return None
