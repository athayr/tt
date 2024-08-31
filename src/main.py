from src.core.config import settings
from src.crud.task_repository import TaskRepository
from src.domain.task import Task, TaskBase, TaskCreate, TaskUpdate
from src.infrastructure.db.session import get_session

if __name__ == '__main__':
    print(settings.database_uri)

    db_session = next(get_session())

    task = TaskBase(title='Title', description='Description')

    task_repository = TaskRepository(db_session)

    nt = task_repository.add(TaskCreate(**task.model_dump(), user='athayr'))
    print(nt)

    gnt = task_repository.get(nt.id)

    lat = task_repository.list()

    lut = task_repository.update(TaskUpdate(title='updated'), task_id=nt.id)

    task_repository.delete(nt.id)

    print(task)
