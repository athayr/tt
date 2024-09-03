from datetime import datetime
from unittest.mock import MagicMock, patch

from src.crud.task_repository import TaskRepository
from src.domain.task import Task, TaskCreate, TaskStatus
from src.models.task_model import TaskModel


def test_create_task_cenario1():
    mock_session = MagicMock()

    task_data = TaskCreate(
        title='Título da Tarefa',
        description='Descrição da Tarefa',
        user='user1',
    )

    mock_task_model = TaskModel(
        id=1,
        title=task_data.title,
        description=task_data.description,
        user=task_data.user,
        status=TaskStatus.PENDING,
        created_at=datetime.utcnow(),
    )

    mock_task = Task(
        id=1,
        title='Título da Tarefa',
        description='Descrição da Tarefa',
        user='user1',
        status=TaskStatus.PENDING,
        created_at=datetime.utcnow(),
        completed_at=None,
    )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    with patch(
        'src.models.task_model.TaskModel', return_value=mock_task_model
    ):
        with patch(
            'src.domain.task.Task.model_validate', return_value=mock_task
        ):
            repository = TaskRepository(mock_session)
            result = repository.add(task_data)

            task = Task.model_validate(result)

            # Verifique se o método add foi chamado corretamente
            # mock_session.add.assert_called_once_with(mock_task_model)
            # mock_session.commit.assert_called_once()

            assert isinstance(task, Task)
            assert result.title == 'Título da Tarefa'
            assert result.description == 'Descrição da Tarefa'
            assert result.user == 'user1'
            assert result.status == TaskStatus.PENDING
