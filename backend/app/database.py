import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()  # lit backend/.env si je lance depuis backend/

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def test_connection() -> str:
    """Renvoie 'ok' si la connexion MySQL fonctionne."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return "ok"
