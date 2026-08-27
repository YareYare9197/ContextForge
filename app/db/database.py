import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing")

# Engine manages database connections and the connection pool.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# SessionLocal will later be used for database queries and transactions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def check_database_connection():
    # Opens one connection from the pool.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))