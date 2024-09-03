from src.cli import (
    _list_all_tasks,
    cancel_task,
    complete_task,
    delete_task,
    list_canceled_tasks,
    list_complete_tasks,
    list_pending_tasks,
)
from src.core.utils import _exit, clear_terminal, invalid_option, show_menu
from src.services.task_service import add_task, update_one_task
from src.create_db import create_tables

OPTIONS = {
    '0': _exit,
    '1': add_task,
    '2': _list_all_tasks,
    '3': complete_task,
    '4': cancel_task,
    '5': delete_task,
    '6': list_canceled_tasks,
    '7': list_complete_tasks,
    '8': list_pending_tasks,
    '9': update_one_task,
}

if __name__ == '__main__':
    create_tables()
    while True:
        show_menu()
        option = input('Digite uma opção válida: ')

        func = OPTIONS.get(option, invalid_option)

        func()

        input('\nPressione Enter para voltar ao menu...')
        clear_terminal()
