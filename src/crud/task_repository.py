from sqlalchemy import Row, RowMapping, and_, delete, desc, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.crud.repository import Repository
from src.domain.task import Task, TaskCreate, TaskUpdate
from src.models.task_model import TaskModel


class TaskRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, task: TaskCreate) -> Task:
        task_model = TaskModel(**task.model_dump())
        self.session.add(task_model)
        self.session.commit()
        return Task.model_validate(task_model)

    def get(self, task_id: int) -> Task | None:
        query = select(TaskModel).where(task_id == TaskModel.id)
        task_model = self.session.execute(query)
        if _result := task_model.scalar():
            return Task.model_validate(_result)
        return None

    def list(self) -> list[Task]:
        query = select(TaskModel)
        task_models = self.session.execute(query).scalars()
        return [Task.model_validate(task_model) for task_model in task_models]

    def update(self, task: TaskUpdate, task_id: int) -> Task:
        in_schema = task.model_dump(exclude_none=True)

        task_model = self.session.execute(
            update(TaskModel)
            .where(task_id == TaskModel.id)
            .values(**in_schema)
            .returning(TaskModel)
        )
        if _result := task_model.scalar():
            self.session.commit()
            return Task.model_validate(_result)

    def delete(self, task_id: int) -> None:
        query = (
            delete(TaskModel)
            .where(task_id == TaskModel.id)
            .returning(TaskModel)
        )
        task_model = self.session.execute(query)
        if task_model.scalar():
            self.session.commit()
