![logo](assets/tasks.png){ width="200" .center }
# Task Management Application

Esta é uma aplicação de gerenciamento de tarefas que utiliza Python e PostgreSQL, executada em contêineres Docker. Este documento descreve o processo para configurar e executar a aplicação.

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

OU

- [python](https://www.python.org/downloads/)
- [postgres](https://www.postgresql.org)

## Configuração do Projeto

### Estrutura do Projeto

A estrutura do projeto segue este formato:

```none
task_management/
├── README.md
├── docs
│   ├── assets
│   │   └── tasks.png
│   ├── index.md
│   └── stylesheets
│       └── extra.css
├── mkdocs.yml
├── poetry.lock
├── pyproject.toml
├── requirements
│   └── base.py
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── cli.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── rich_table.py
│   ├── create_db.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   └── task_repository.py
│   ├── domain
│   │   ├── __init__.py
│   │   └── task.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   └── db
│   │       ├── __init__.py
│   │       └── session.py
│   ├── main.py
│   └── models
│       ├── __init__.py
│       └── task_model.py
└── tests
    └── __init__.py
```

### Arquivo Dockerfile

O `Dockerfile` está configurado para:

1. Usar a imagem oficial do Python 3.11 slim.
2. Definir o diretório de trabalho como `/app`.
3. Instalar as dependências para rodar o projeto listadas em `requirements/base.txt`.
4. Copiar todos os arquivos da aplicação para o contêiner.
5. Executar o script de criação do banco de dados (`create_db.py`) e, em seguida, iniciar a aplicação (`main.py`).

### Arquivo docker-compose.yml

O `compose.yaml` está configurado para:

1. Criar e configurar um serviço PostgreSQL com as credenciais fornecidas.
2. Construir a imagem da aplicação Python.
3. Executar o comando que inicializa o banco de dados e, em seguida, a aplicação.

### Variáveis de Ambiente

As variáveis de ambiente são configuradas no `docker-compose.yml`, incluindo:

- `DATABASE_URI`: A URI de conexão com o banco de dados PostgreSQL.

## Instruções para Execução com Docker

### Passo 1: Clonar o Repositório

Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/athayr/tt task_management
cd task_management
```

### Passo 2: Construir e Executar a Aplicação

Use o Docker Compose para construir e executar os contêineres:

```bash
docker compose up --build
```

Esse comando:

1. Baixará a imagem do PostgreSQL e criará o contêiner do banco de dados.
2. Construirá a imagem Docker da aplicação Python.
3. Executará o script `create_db.py` para configurar o banco de dados.
4. Iniciará a aplicação principal.

### Passo 3: Interagir com a Aplicação

Após iniciar a aplicação, você pode interagir com ela através do terminal.

Dependendo do seu sistema operacional você precisará executar alguns comandos adicionais

#### Passo 3.1: Entrar na "maquina" docker
Execute o seguinte comando no seu terminal

```bash
docker exec -it task_management bash
```

Após está na maquina docker do docker basta digitar o seguinte comando para exibir o menu de opções

```bash
tasks
```

Caso queira usar o cli você pode ver todos os comandos possiveis com esse comando

```bash
task --help
```

Se precisar parar a aplicação:

```bash
docker-compose down
```

Isso encerrará e removerá todos os contêineres relacionados à aplicação.

## Debug e Logs

Você pode visualizar os logs da aplicação em tempo real usando:

```bash
docker-compose logs -f
```

## Considerações Finais

Este repositório foi configurado para permitir fácil configuração e execução da aplicação de gerenciamento de tarefas em um ambiente isolado usando Docker. Certifique-se de verificar se todas as dependências e credenciais estão corretas antes de executar a aplicação.

Para mais detalhes ou contribuições, por favor, abra uma [issue](https://github.com/athayr/tt/issues) ou envie um [pull request](https://github.com/athayr/tt/pulls).
