from abc import ABC, abstractmethod

from src.domain.task import Task


class Repository(ABC):
    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def get(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def list(self) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass
