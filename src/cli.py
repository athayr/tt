import typer
from rich import pretty
from rich.console import Console

from src.core.rich_table import task_table, users_table
from src.crud.task_repository import TaskRepository
from src.domain.task import TaskCreate, TaskStatus, TaskUpdate
from src.infrastructure.db.session import get_session

app = typer.Typer()
console = Console()

users_distinct = {-1: 'default', -2: 'outro'}


@app.command()
def create_task(
    title: str = 'title',
    description: str = 'description',
    user: str | None = None,
):
    db = next(get_session())
    repository = TaskRepository(db)

    if not user:
        users = repository.distinct_user()
        for key, db_user in enumerate(users):
            if db_user.lower() != 'default':
                users_distinct.update({key: db_user.lower()})

        pretty.install()
        users_table('Users list', users_distinct)
        index = int(input('Selectione um responsavel, use a chave: '))

        if index == -2:
            user = input('Qual o nome do responsavel? ')
        else:
            user = users_distinct[index]

    task = TaskCreate(title=title, description=description, user=user.lower())
    repository.add(task)
    console.print(f"Tarefa '{title}' criada com sucesso!", style='bold green')


@app.command()
def list_all_tasks():
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


@app.command()
def update_task(title: str = None, description: str = None):
    list_all_tasks()
    task_id = int(input('Qual Id deseja atualizar? '))

    db = next(get_session())

    repository = TaskRepository(db)
    task = TaskUpdate(title=title, description=description)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        console.print(
            f'Tarefa com ID {task_id} excluída com sucesso!',
            style='bold green',
        )
    else:
        console.print(
            f'Tarefa com ID {task_id} não encontrada.', style='bold red'
        )


@app.command()
def delete_task():
    list_all_tasks()
    task_id = int(input('Qual Id deseja remover? '))

    db = next(get_session())
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

    repository = TaskRepository(db)
    task = TaskUpdate(status=TaskStatus.COMPLETED)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        console.print(
            f"Tarefa '{task_udpdated.title}' atualizada com sucesso!",
            style='bold green',
        )
    else:
        console.print(
            f'Tarefa com ID {task_id} não encontrada.', style='bold red'
        )


@app.command()
def cancel_task():
    list_pending_tasks()
    task_id = int(input('Qual Id deseja cancelar? '))

    db = next(get_session())

    repository = TaskRepository(db)
    task = TaskUpdate(status=TaskStatus.CANCELLED)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        console.print(
            f"Tarefa '{task_udpdated.title}' atualizada com sucesso!",
            style='bold green',
        )
    else:
        console.print(
            f'Tarefa com ID {task_id} não encontrada.', style='bold red'
        )


if __name__ == '__main__':
    app()
