from typing import Any

from rich import box
from rich.console import Console
from rich.table import Table

from src.domain.task import Task


def task_table(title: str, tasks: list[Task]) -> None:
    table = Table(title=title, box=box.MINIMAL_DOUBLE_HEAD)

    table.add_column('ID', justify='right', style='cyan', no_wrap=True)
    table.add_column('Title', style='magenta')
    table.add_column('Description', width=50, style='magenta')
    table.add_column('STATUS', justify='right', style='green')

    for task in tasks:
        table.add_row(
            str(task.id), task.title, task.description, task.status.name
        )

    console = Console()
    console.print(table)


def users_table(title: str, users: dict[int, str]) -> None:
    table = Table(title=title, box=box.MINIMAL_DOUBLE_HEAD)

    table.add_column('ID', justify='right', style='cyan', no_wrap=True)
    table.add_column('Name', style='magenta')

    for key, user in users.items():
        table.add_row(str(key), user)

    console = Console()
    console.print(table)


def render_table(
    title: str,
    columns: dict[str, dict[str, str | bool]],
    values: list[list[str]],
) -> None:
    table = Table(title=title)

    for title, kwargs in columns.items():
        table.add_column(title, **kwargs)

    for value in values:
        table.add_row(*value)

    console = Console()
    console.print(table)
