import pandas

from src.data.schemas import QTotalSchema, FilterSchema


class DataServiceProtocol:
    async def get_q_total(self, filters: FilterSchema) -> list[QTotalSchema]:
        raise NotImplementedError

    async def upload_data_to_db(self, data: pandas.DataFrame) -> None:
        raise NotImplementedError
