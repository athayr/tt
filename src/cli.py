import typer

from src.crud.task_repository import TaskRepository
from src.domain.task import TaskCreate, TaskStatus, TaskUpdate
from src.infrastructure.db.session import get_session

app = typer.Typer()

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
            users_distinct.update({key: db_user.lower()})

        print(users_distinct)
        index = int(input('Selectione um responsavel, use a chave: '))

        if index == -2:
            user = input('Qual o nome do responsavel? ')
        else:
            user = users_distinct[index]

    task = TaskCreate(title=title, description=description, user=user.lower())
    repository.add(task)
    typer.echo(f"Tarefa '{title}' criada com sucesso!")


@app.command()
def list_all_tasks():
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list()
    if tasks:
        for task in tasks:
            typer.echo(f'{task.id}: {task.title} - {task.status}')
    else:
        typer.echo('Nenhuma tarefa encontrada.')


@app.command()
def list_complete_tasks():
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list_by_status(TaskStatus.COMPLETED)
    if tasks:
        for task in tasks:
            typer.echo(f'{task.id}: {task.title} - {task.status}')
    else:
        typer.echo('Nenhuma tarefa encontrada.')


@app.command()
def list_canceled_tasks():
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list_by_status(TaskStatus.CANCELLED)
    if tasks:
        for task in tasks:
            typer.echo(f'{task.id}: {task.title} - {task.status}')
    else:
        typer.echo('Nenhuma tarefa encontrada.')


@app.command()
def list_pending_tasks():
    db = next(get_session())
    repository = TaskRepository(db)
    tasks = repository.list_by_status(TaskStatus.PENDING)
    if tasks:
        for task in tasks:
            typer.echo(f'{task.id}: {task.title} - {task.status}')
    else:
        typer.echo('Nenhuma tarefa encontrada.')


@app.command()
def update_task(title: str = None, description: str = None):
    list_all_tasks()
    task_id = int(input('Qual Id deseja atualizar? '))

    db = next(get_session())

    repository = TaskRepository(db)
    task = TaskUpdate(title=title, description=description)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        typer.echo(f"Tarefa '{task_udpdated.title}' atualizada com sucesso!")
    else:
        typer.echo(f'Tarefa com ID {task_id} não encontrada.')


@app.command()
def delete_task():
    list_all_tasks()
    task_id = int(input('Qual Id deseja remover? '))

    db = next(get_session())
    repository = TaskRepository(db)
    repository.delete(task_id)
    typer.echo(f'Tarefa com ID {task_id} excluída com sucesso!')


@app.command()
def complete_task():
    list_pending_tasks()
    task_id = int(input('Qual Id deseja finalizar? '))

    db = next(get_session())

    repository = TaskRepository(db)
    task = TaskUpdate(status=TaskStatus.COMPLETED)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        typer.echo(f"Tarefa '{task_udpdated.title}' atualizada com sucesso!")
    else:
        typer.echo(f'Tarefa com ID {task_id} não encontrada.')


@app.command()
def cancel_task():
    list_pending_tasks()
    task_id = int(input('Qual Id deseja cancelar? '))

    db = next(get_session())

    repository = TaskRepository(db)
    task = TaskUpdate(status=TaskStatus.CANCELLED)
    task_udpdated = repository.update(task, task_id)

    if task_udpdated:
        typer.echo(f"Tarefa '{task_udpdated.title}' atualizada com sucesso!")
    else:
        typer.echo(f'Tarefa com ID {task_id} não encontrada.')


if __name__ == '__main__':
    app()
