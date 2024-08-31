from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.crud.repository import Repository
from src.domain.task import Task, TaskCreate, TaskStatus, TaskUpdate
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

    def distinct_user(self) -> Sequence[Row[Any] | RowMapping | Any]:
        query = select(TaskModel.user.distinct())
        distinct_users = self.session.execute(query)
        if _result := distinct_users.scalars():
            return _result.all()

    def list_by_user(self, user: str) -> list[Task | None]:
        query = select(TaskModel).where(user == TaskModel.user)
        task_models = self.session.execute(query).scalars()
        return [Task.model_validate(task_model) for task_model in task_models]

    def list_by_status(self, status: TaskStatus) -> list[Task]:
        query = select(TaskModel).where(TaskModel.status == status)
        task_models = self.session.execute(query).scalars()
        return [Task.model_validate(task_model) for task_model in task_models]

    def list(self) -> list[Task]:
        query = select(TaskModel)
        task_models = self.session.execute(query).scalars()
        return [Task.model_validate(task_model) for task_model in task_models]

    def update(self, task: TaskUpdate, task_id: int) -> Task | None:
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

        return

    def delete(self, task_id: int) -> None:
        query = (
            delete(TaskModel)
            .where(task_id == TaskModel.id)
            .returning(TaskModel)
        )
        task_model = self.session.execute(query)
        if task_model.scalar():
            self.session.commit()

        return
