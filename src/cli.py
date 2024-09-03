import typer

from src.core.rich_table import task_table
from src.core.utils import console, task_message
from src.crud.task_repository import TaskRepository
from src.domain.task import TaskStatus, TaskUpdate
from src.infrastructure.db.session import get_session
from src.services.task_service import create_task, list_all_tasks, update_task
from src.create_db import create_tables

app = typer.Typer()


@app.command('create-task')
def new_task(
    title: str = 'title',
    description: str = 'description',
    user: str | None = None,
):
    db = next(get_session())
    create_task(db, title=title, description=description, user=user)


@app.command('list-all-tasks')
def _list_all_tasks():
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list()

    if tasks:
        task_table('All Tasks', tasks)
    else:
        console.print('Nenhuma tarefa encontrada.', style='bold red')


@app.command()
def list_complete_tasks():
    db = next(get_session())
    repository = TaskRepository(db)

    tasks = repository.list_by_status(TaskStatus.COMPLETED)

    if tasks:
        task_table('Complete Tasks', tasks)
    else:
        console.print('Nenhuma tarefa encontrada.', style='bold red')


@app.command()
def list_canceled_tasks():
    db = next(get_session())
    repository = TaskRepository(db)

    tasks = repository.list_by_status(TaskStatus.CANCELLED)

    if tasks:
        task_table('Canceled Tasks', tasks)
    else:
        console.print('Nenhuma tarefa encontrada.', style='bold red')


@app.command()
def list_pending_tasks():
    db = next(get_session())
    repository = TaskRepository(db)

    tasks = repository.list_by_status(TaskStatus.PENDING)

    if tasks:
        task_table('Pending Tasks', tasks)
    else:
        console.print('Nenhuma tarefa encontrada.', style='bold red')


@app.command('update-task')
def _update_task(title: str = None, description: str = None):
    db = next(get_session())
    tasks = list_all_tasks(db)

    if tasks:
        task_table('Canceled Tasks', tasks)

    task_id = int(input('Qual Id deseja atualizar? '))

    task = TaskUpdate(title=title, description=description)
    update_task(db=db, task=task, task_id=task_id)


@app.command()
def delete_task():
    db = next(get_session())
    tasks = list_all_tasks(db)

    if tasks:
        task_table('Canceled Tasks', tasks)

    task_id = int(input('Qual Id deseja remover? '))

    repository = TaskRepository(db)
    repository.delete(task_id)
    console.print(
        f'Tarefa com ID {task_id} excluída com sucesso!', style='bold green'
    )


@app.command()
def complete_task():
    list_pending_tasks()
    task_id = int(input('Qual Id deseja finalizar? '))

    db = next(get_session())

    task = TaskUpdate(status=TaskStatus.COMPLETED)
    task_updated = update_task(db=db, task=task, task_id=task_id)
    task_message(task_updated, task_id)


@app.command()
def cancel_task():
    list_pending_tasks()
    task_id = int(input('Qual Id deseja cancelar? '))

    db = next(get_session())

    task = TaskUpdate(status=TaskStatus.CANCELLED)
    task_updated = update_task(db=db, task=task, task_id=task_id)
    task_message(task_updated, task_id)


if __name__ == '__main__':
    create_tables()
    app()
