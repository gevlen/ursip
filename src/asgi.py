from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.data.router import data_router
from src.database import create_database_url
from src.database.settings import db_name
from src.data.controler import DataService
from src.data.protocol import DataServiceProtocol


def create_application() -> FastAPI:
    application = FastAPI(
        title="Data-Service",
        debug=False,
    )
    application.include_router(data_router)

    engine = create_async_engine(
        create_database_url(db_name),
        echo=True,
    )
    async_session = async_sessionmaker(engine)
    data_service = DataService(async_session)
    application.dependency_overrides[DataServiceProtocol] = lambda: data_service

    return application


app = create_application()


@app.get("/ping/")
async def root() -> str:
    return "pong"
