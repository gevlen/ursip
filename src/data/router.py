import pathlib

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import ORJSONResponse

from src.data.protocol import DataServiceProtocol
from src.data.schemas import FilterSchema, QTotalSchema, ErrorSchema
from src.data.interactor import get_pandas_data_frame, excel_extensions
from src.services.excel_converter import TestDataExcelConverter

data_router = APIRouter(tags=["data"], prefix="/data")


@data_router.get(path="/", responses={200: {"model": list[QTotalSchema]}})
async def get_q_total(
    filters: FilterSchema = Depends(), data_service: DataServiceProtocol = Depends()
):
    q_totals = await data_service.get_q_total(filters)
    return ORJSONResponse(content=[q_total.dict() for q_total in q_totals])


@data_router.post(
    path="/",
    responses={200: {"model": list[QTotalSchema]}, 400: {"model": ErrorSchema}},
)
async def upload_excel_file(
    file: UploadFile, data_service: DataServiceProtocol = Depends()
):
    file_extension = pathlib.Path(file.filename if file.filename else "").suffix
    if file_extension not in excel_extensions:
        return ORJSONResponse(
            status_code=400,
            content={"detail": f"Wrong file extension. Expected {excel_extensions}"},
        )
    data = get_pandas_data_frame(file.file, converter=TestDataExcelConverter())
    if data is None:
        return ORJSONResponse(
            status_code=400, content={"detail": "Wrong excel file structure"}
        )
    await data_service.upload_data_to_db(data)
