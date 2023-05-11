import datetime

from pydantic import BaseModel, Field


class QTotalSchema(BaseModel):
    date: datetime.date
    q_type: str | None
    data_type: str | None
    company: str | None
    fact_plan_type: str | None
    total_data: int = Field(alias="data")


class FilterSchema(BaseModel):
    q_type: bool = Field(default=True)
    data_type: bool = Field(default=False)
    company: bool = Field(default=False)
    fact_plan_type: bool = Field(default=True)


class ErrorSchema(BaseModel):
    detail: str
