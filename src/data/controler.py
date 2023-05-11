from typing import TypeVar

import pandas
import sqlalchemy
from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database.models import TestTable, QType, FactPlanType, Company, DataType
from src.data.schemas import QTotalSchema, FilterSchema


T = TypeVar("T")


class DataService:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]) -> None:
        self._session = async_session

    async def get_q_total(self, filters: FilterSchema) -> list[QTotalSchema]:
        query = self._get_q_total_query(filters.dict())
        async with self._session() as session:
            async with session.begin():
                q_total = await session.execute(query)
                return [QTotalSchema(**data._asdict()) for data in q_total]

    def _get_q_total_query(self, filters: dict[str, bool]) -> Select:
        data: dict[
            str, type[QType] | type[FactPlanType] | type[Company] | type[DataType]
        ] = {
            "q_type": QType,
            "fact_plan_type": FactPlanType,
            "company": Company,
            "data_type": DataType,
        }
        query = select(
            TestTable.date,
            func.sum(TestTable.data).label("data"),
            *(data[key].name.label(key) for key, value in filters.items() if value)
        )
        for key, value in filters.items():
            if value:
                query = query.join(data[key])
        query = query.group_by(
            TestTable.date, *(data[key].name for key, value in filters.items() if value)
        )
        return query

    async def upload_data_to_db(self, data: pandas.DataFrame):
        async with self._session() as session:
            async with session.begin():
                for i in data.index:
                    test_table = TestTable(
                        data=int(data["value"][i]),
                        date=data["date"][i],
                        company=await self._execute_entity(
                            data["company"][i], Company, session
                        ),
                        data_type=await self._execute_entity(
                            data["data_type"][i], DataType, session
                        ),
                        q_type=await self._execute_entity(
                            data["q_type"][i], QType, session
                        ),
                        fact_plan_type=await self._execute_entity(
                            data["plan_fact"][i], FactPlanType, session
                        ),
                    )
                    session.add(test_table)

    async def _execute_entity(self, name: str, model, session: AsyncSession):
        entity = await session.execute(select(model).where(model.name == name))
        try:
            entity = entity.scalars().one()
            return entity
        except sqlalchemy.exc.NoResultFound:
            entity = model(name=name)
            session.add(entity)
            return entity
