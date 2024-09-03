from rich.console import Console
from sqlalchemy.orm import Session

from src.core.rich_table import render_table
from src.core.utils import TASK_COLUMNS, USER_COLUMNS, task_message
from src.crud.task_repository import TaskRepository
from src.domain.task import Task, TaskCreate, TaskStatus, TaskUpdate
from src.infrastructure.db.session import get_session

users_distinct = {'-1': 'default', '-2': 'outro'}
console = Console()


def add_task():
    title = input('Digite o título da tarefa: ')
    description = input('Digite a descrição da tarefa: ')
    user = input(
        'Digite o responsável pela tarefa '
        '(ou deixe em branco para escolher depois): '
    )
    db = next(get_session())
    create_task(db=db, title=title, description=description, user=user or None)


def update_one_task():
    title = input('Digite o novo título (ou deixe em branco para pular): ')
    description = input(
        'Digite a nova descrição (ou deixe em branco para pular): '
    )
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list_by_status(TaskStatus.PENDING)
    if tasks:
        values = [
            [str(task.id), task.title, task.description, task.status.name]
            for task in tasks
        ]
        render_table('Pending Tasks', columns=TASK_COLUMNS, values=values)
    else:
        console.print('Nenhuma tarefa encontrada.', style='bold red')

    task_id = int(input('Qual Id deseja finalizar? '))

    task = TaskUpdate(title=title, description=description)
    task_updated = update_task(db=db, task=task, task_id=task_id)
    task_message(task_updated, task_id)


def create_task(
    db: Session,
    title: str = 'title',
    description: str = 'description',
    user: str | None = None,
):
    repository = TaskRepository(db)

    if not user:
        users = repository.distinct_user()
        for key, db_user in enumerate(users):
            if db_user.lower() != 'default':
                users_distinct.update({str(key): db_user.lower()})

        values = [[str(key), value] for key, value in users_distinct.items()]
        render_table('Users list', columns=USER_COLUMNS, values=values)
        index = input('Selectione um responsavel, use a chave: ')

        if index == '-2':
            user = input('Qual o nome do responsavel? ')
        else:
            user = users_distinct.get(index)

        if not user:
            console.print('Usuario invalido!', style='bold red')
            return

    task = TaskCreate(title=title, description=description, user=user.lower())
    repository.add(task)
    console.print(f"Tarefa '{title}' criada com sucesso!", style='bold green')


def update_task(db: Session, task: TaskUpdate, task_id: int = None):
    repository = TaskRepository(db)
    return repository.update(task, task_id)


def list_all_tasks(
    db: Session,
) -> list[Task]:
    repository = TaskRepository(db)
    return repository.list()
