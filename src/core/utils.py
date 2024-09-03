import os

from rich.console import Console

from src.core.rich_table import render_table
from src.domain.task import Task

console = Console()

DATA_COLUMNS = {'ID': dict(justify='right', style='cyan', no_wrap=True)}

TASK_COLUMNS = DATA_COLUMNS.copy()
TASK_COLUMNS.update(
    {
        'Title': dict(style='magenta'),
        'Description': dict(width=50, style='magenta'),
        'STATUS': dict(justify='right', style='green'),
    }
)

USER_COLUMNS = DATA_COLUMNS.copy()
USER_COLUMNS.update(
    {
        'Name': dict(width=50, style='magenta'),
    }
)


def _exit():
    exit(1)


def invalid_option():
    print('Opção inválida', 'Por favor, tente novamente.')


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    columns = {
        'Opção': dict(justify='right', style='cyan', no_wrap=True),
        'Ação': dict(width=50, style='magenta'),
    }
    values = [
        ['1', 'Criar Tarefa'],
        ['2', 'Listar Todas as Tarefas'],
        ['3', 'Concluir Tarefa'],
        ['4', 'Cancelar Tarefa'],
        ['5', 'Deletar Tarefa'],
        ['6', 'Listar Tarefas Canceladas'],
        ['7', 'Listar Tarefas Concluídas'],
        ['8', 'Listar Tarefas Pendentes'],
        ['9', 'Atualizar Tarefa'],
        ['0', 'Sair'],
    ]
    render_table('Menu', columns=columns, values=values)


def task_message(task: Task | None, task_id: int):
    if task:
        console.print(
            f"Tarefa '{task.title}' atualizada com sucesso!",
            style='bold green',
        )
    else:
        console.print(
            f'Tarefa com ID {task_id} não encontrada.', style='bold red'
        )
