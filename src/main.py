from src.core.config import settings
from src.domain.task import Task, TaskCreate, TaskStatus


if __name__ == '__main__':
    print(settings.database_uri)
    task = TaskCreate(title='Title', description='Description')
    print(task)

