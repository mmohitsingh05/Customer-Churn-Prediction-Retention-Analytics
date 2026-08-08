import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_engine():
    """Return SQLAlchemy engine for churn_analytics database."""
    encoded_password = quote_plus(DB_PASSWORD or "")
    url = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)


def get_connection():
    """Return psycopg2 connection for churn_analytics database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )


if __name__ == "__main__":
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(__import__("sqlalchemy").text("SELECT 1"))
            print("SQLAlchemy connection: OK")
    except Exception as e:
        print(f"SQLAlchemy error: {e}")

    try:
        conn = get_connection()
        conn.close()
        print("psycopg2 connection: OK")
    except Exception as e:
        print(f"psycopg2 error: {e}")
