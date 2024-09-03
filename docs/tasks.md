# Funções de Tarefas

Este documento descreve as funções responsáveis por criar, atualizar e manipular tarefas no sistema.

## `create_task`

```python
def create_task(
db: Session,
title: str = 'title',
description: str = 'description',
user: str | None = None,
):
"""
Cria uma nova tarefa no banco de dados.
"""
```

**Descrição:**

Esta função cria uma nova tarefa no banco de dados.

**Parâmetros:**

- `db`: Sessão do banco de dados.
- `title`: Título da tarefa.
- `description`: Descrição da tarefa.
- `user`: Responsável pela tarefa (opcional).

**Retorno:**

- `None`

**Exemplo de uso:**

```python
db = get_db_session()
create_task(db, title="Nova Tarefa", description="Descrição da tarefa", user="joao")
```

**Validação:**

Esta função cria uma nova tarefa no banco de dados e valida se o usuário existe. Caso o usuário não seja passado, a função solicitará a escolha de um usuário.
