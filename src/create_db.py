import time
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import inspect

from src.infrastructure.db.session import engine
from src.models.task_model import Base
from src.core.config import settings


def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(settings.database_uri)
            conn.close()
            break
        except OperationalError:
            print("Esperando pelo banco de dados...")
            time.sleep(2)


def create_tables():
    wait_for_postgres()
    inspector = inspect(engine)

    existing_tables = inspector.get_table_names()

    all_tables = Base.metadata.tables.keys()

    missing_tables = [
        table for table in all_tables if table not in existing_tables
    ]

    if missing_tables:
        print(f"Tabelas ausentes encontradas: {missing_tables}")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas!")


if __name__ == '__main__':
    create_tables()
