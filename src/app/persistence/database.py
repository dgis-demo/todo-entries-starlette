from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "db.sqlite3"

session_maker = sessionmaker(
    bind=create_engine(f"sqlite:///{DB_PATH}"),
)
