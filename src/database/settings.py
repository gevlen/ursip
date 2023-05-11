import os
from pathlib import Path

db_name = os.getenv("DB_NAME", "test_db.db")


def create_database_url(filepath: Path | str) -> str:
    return f"sqlite+aiosqlite:///{filepath}"
