from datetime import datetime

from sqlalchemy import String, ForeignKey, Date, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class TestTable(Base):
    __tablename__ = "test_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[datetime] = mapped_column(Date())

    data: Mapped[int] = mapped_column(Integer)

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship(back_populates="test_table")

    data_type_id: Mapped[int] = mapped_column(ForeignKey("data_type.id"))
    data_type: Mapped["DataType"] = relationship(back_populates="test_table")

    q_type_id: Mapped[int] = mapped_column(ForeignKey("q_type.id"))
    q_type: Mapped["QType"] = relationship(back_populates="test_table")

    fact_plan_type_id: Mapped[int] = mapped_column(ForeignKey("fact_plan_type.id"))
    fact_plan_type: Mapped["FactPlanType"] = relationship(back_populates="test_table")


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    test_table: Mapped[list["TestTable"]] = relationship(back_populates="company")


class DataType(Base):
    __tablename__ = "data_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    test_table: Mapped[list["TestTable"]] = relationship(back_populates="data_type")


class QType(Base):
    __tablename__ = "q_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    test_table: Mapped[list["TestTable"]] = relationship(back_populates="q_type")


class FactPlanType(Base):
    __tablename__ = "fact_plan_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    test_table: Mapped[list["TestTable"]] = relationship(
        back_populates="fact_plan_type"
    )
