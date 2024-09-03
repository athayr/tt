from datetime import datetime
from enum import Enum, auto

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = auto()
    CANCELLED = auto()
    COMPLETED = auto()


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    user: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    user: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

    class Config:
        from_attributes = True
