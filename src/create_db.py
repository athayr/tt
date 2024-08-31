from src.infrastructure.db.session import engine
from src.models.task_model import Base


def create_tables():
    Base.metadata.create_all(bind=engine)
    print('Tabelas criadas!')


if __name__ == '__main__':
    create_tables()
