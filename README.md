# Task Manager API

Uma API RESTful para gerenciamento de tarefas, comentários e usuários, com autenticação JWT.

---

## Índice

- [Visão Geral](#visão-geral)  
- [Funcionalidades](#funcionalidades)  
- [Tecnologias](#tecnologias)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Configuração](#configuração)  
- [Execução](#execução)  
- [Endpoints](#endpoints)  
  - [Autenticação](#autenticação)  
  - [Usuários](#usuários)  
  - [Tarefas](#tarefas)  
  - [Comentários](#comentários)  
- [Logging](#logging)  
- [Banco de Dados](#banco-de-dados)  
- [Testes](#testes)  
- [Contribuição](#contribuição)  
- [Licença](#licença)  

---

## Visão Geral

Este projeto implementa um sistema de **Task Manager** usando **FastAPI**, **SQLAlchemy** e **JWT** para autenticação. Permite criar, listar, atualizar e excluir usuários e tarefas, além de adicionar comentários às tarefas.

---

## Funcionalidades

- **Autenticação JWT** (login e logout)  
- **CRUD de Usuários** (create, read, update, soft delete)  
- **CRUD de Tarefas** (create, read, update, delete, filtros por status/priority/due_date/assigned_to)  
- **CRUD de Comentários** associados a tarefas  
- **Logging** estruturado com console e arquivo rotativo  
- **Validações de negócio** (status e prioridade de tarefas, datas, e-mails únicos)  
- **Testes automatizados** com pytest  

---

## Tecnologias

- Python 3.10+  
- FastAPI  
- SQLAlchemy  
- SQLite (ou outro banco configurável)  
- passlib (bcrypt) para hashing de senhas  
- PyJWT para tokens JWT  
- Uvicorn como servidor ASGI  
- pytest para testes  

---

## Pré-requisitos

- Git  
- Python 3.10+ 

---

## Dependências

Instale as bibliotecas necessárias via pip:

```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] PyJWT pytest
```

Se preferir, crie um arquivo `requirements.txt` com:

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
passlib[bcrypt]
PyJWT
pytest
```

E instale com:

```bash
pip install -r requirements.txt
```

---

## Instalação

1. Clone o repositório:  
   ```bash
   git clone https://github.com/seu-usuario/tasks-manager.git
   cd tasks-manager
   ```

2. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

- **Variáveis de ambiente**  
  - `JWT_SECRET`: chave secreta para geração de tokens (padrão: `supersecret`)  
  - `DATABASE_URL`: URL de conexão SQLAlchemy (padrão: `sqlite:///./app.db`)  

- **Logs**  
  A pasta `logs/` é criada automaticamente na primeira execução e contém `app.log` rotacionado diariamente.

---

## Execução

```bash
python -m src.main
```

O servidor ficará disponível em `http://localhost:8000/docs`.

---

## Endpoints

### Autenticação

| Método | Rota           | Descrição                     | Corpo / Query                         |
| ------ | -------------- | ----------------------------- | ------------------------------------- |
| POST   | `/auth/login`  | Autentica e obtém token JWT   | `{ "username": "...", "password": "..." }` |
| GET    | `/auth/logout` | Logout (endpoint simulado)    | —                                     |

### Usuários

| Método | Rota                 | Descrição                           | Corpo                                   |
| ------ | -------------------- | ----------------------------------- | --------------------------------------- |
| POST   | `/users/`            | Cria novo usuário                   | `{ "name": "", "email": "", "password": "" }` |
| GET    | `/users/{user_id}`   | Obtém dados de um usuário ativo     | —                                       |
| PUT    | `/users/{user_id}`   | Atualiza nome, e-mail ou senha      | `{ "name"?, "email"?, "password"? }`    |
| DELETE | `/users/{user_id}`   | Desativa usuário (soft delete)      | —                                       |

### Tarefas

| Método | Rota                         | Descrição                                     | Corpo / Query                                   |
| ------ | ---------------------------- | --------------------------------------------- | ----------------------------------------------- |
| POST   | `/tasks/`                    | Cria nova tarefa                              | `{ "title": "", "due_date"?, "priority"?, "status"?, "assigned_to"? }` |
| GET    | `/tasks/{task_id}`           | Obtém uma tarefa por ID                       | —                                               |
| GET    | `/tasks/?assigned_to={user}` | Lista tarefas de um usuário                   | —                                               |
| PUT    | `/tasks/{task_id}`           | Atualiza campos de uma tarefa                 | `{ "title"?, "due_date"?, "priority"?, "status"?, "assigned_to"? }` |
| DELETE | `/tasks/{task_id}`           | Remove tarefa                                 | —                                               |
| GET    | `/tasks/filter?...`          | Filtra por status, prioridade, due_before, user_id | Query params: `status`, `priority`, `due_before`, `user_id` |

### Comentários

| Método | Rota                                          | Descrição                       | Corpo                                 |
| ------ | --------------------------------------------- | ------------------------------- | ------------------------------------- |
| POST   | `/tasks/{task_id}/comments`                  | Cria comentário em tarefa       | `{ "content": "texto do comentário" }` |
| GET    | `/tasks/{task_id}/comments`                  | Lista comentários de tarefa     | —                                     |
| DELETE | `/tasks/{task_id}/comments/{comment_id}`     | Remove comentário autorizado    | —                                     |

---

## Logging

- **Console**: nível `DEBUG`  
- **Arquivo** (`logs/app.log`): nível `INFO`, rotacionado diariamente, 7 backups  
- **Formato**:  
  ```
  2025-06-18 12:34:56 | INFO     | task_controller | Tarefa criada com sucesso: ID=42
  ```

Use ferramentas como `tail -F logs/app.log`, `grep`, ou lnav para inspeção interativa.

---

## Banco de Dados

Por padrão usa SQLite (`./app.db`). Para trocar:

```bash
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
```

O SQLAlchemy criará tabelas automaticamente no startup.

---

## Testes

Execute toda a suíte com:

```bash
pytest --maxfail=1 --disable-warnings -q
```

Testes de controllers, modelos e rotas estão em `tests/`.

Para verificar a cobertura e demais testes execute:

```bash
pytest --cov=src tests/
```

---

## Contribuição

1. Fork do repositório  
2. Crie uma branch feature: `git checkout -b feature/nome`  
3. Commit suas mudanças: `git commit -m "descrição"`  
4. Push: `git push origin feature/nome`  
5. Abra um Pull Request  

---

## Licença

MIT © Seu Nome
Patrick Borges Wendling e Pedro Lucas Erig Gerhardt