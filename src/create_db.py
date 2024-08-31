from src.models.task_model import Base
from src.infrastructure.db.session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)
    print('Tabelas criadas!')


if __name__ == '__main__':
    create_tables()
