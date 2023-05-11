FROM python:3.11-slim-buster

WORKDIR /

# Dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY migrations/ migrations/
COPY src/ src/
COPY alembic.ini ./alembic.ini
#COPY tests/ tests/