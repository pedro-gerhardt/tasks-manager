# Task Manager API

Uma API RESTful para gerenciamento de tarefas, comentários e usuários, com autenticação JWT.

---

## Índice

- [Visão Geral](#visão-geral)  
- [Decisões Arquiteturais](#decisões-arquiteturais)  
- [Modelagem de Dados](#modelagem-de-dados)  
- [Fluxo de Requisições](#fluxo-de-requisições)  
- [Tecnologias](#tecnologias)  
- [Pré-requisitos](#pré-requisitos)  
- [Dependências](#dependências)  
- [Instalação](#instalação)  
- [Configuração e Deploy](#configuração-e-deploy)  
- [Execução](#execução)  
- [Endpoints](#endpoints)  
  - [Autenticação](#autenticação)  
  - [Usuários](#usuários)  
  - [Tarefas](#tarefas)  
  - [Comentários](#comentários)  
- [Logging](#logging)  
- [Banco de Dados](#banco-de-dados)  
- [Testes Automatizados](#testes-automatizados)  
- [Contribuição](#contribuição)  
- [Licença](#licença)  

---

## Visão Geral

Este projeto implementa um sistema de **Task Manager** usando **FastAPI**, **SQLAlchemy** e **JWT** para autenticação. O objetivo é oferecer uma API simples e robusta para a criação, gerenciamento e acompanhamento de tarefas, com suporte a comentários e permissões básicas de usuário. É indicado para aplicações internas de equipes ou como base para um microserviço de tarefas.

---

## Decisões Arquiteturais

- **Arquitetura em Camadas**: separação clara entre *routers*, *controllers*, *models* e *utils*, facilitando manutenção e testes.  
- **FastAPI + Pydantic**: validação automática de payloads e geração de documentação Swagger.  
- **SQLAlchemy ORM**: mapeamento objeto-relacional para flexibilidade no uso de bancos SQL.  
- **JWT Stateless**: autenticação sem sessão, escalonável para múltiplos nós.  
- **Logging Estruturado**: handlers de console e arquivo com rotação diária, permitindo auditoria e monitoramento.  
- **Princípios de Clean Architecture**: dependências unidirecionais e separação de responsabilidades.

---

## Modelagem de Dados

Entidades principais e seus relacionamentos:

```
Users
  ├─ id (PK, int)
  ├─ name (str)
  ├─ email (str, unique)
  ├─ hashed_password (str)
  ├─ is_active (bool)
  └─ created_at (datetime)

Tasks
  ├─ id (PK, int)
  ├─ title (str)
  ├─ description (str, opcional)
  ├─ due_date (date, opcional)
  ├─ priority (enum: low, medium, high)
  ├─ status (enum: pending, in_progress, done)
  ├─ assigned_to (FK -> users.id, opcional)
  ├─ created_at (datetime)
  └─ updated_at (datetime)

Comments
  ├─ id (PK, int)
  ├─ content (str)
  ├─ task_id (FK -> tasks.id)
  ├─ user_id (FK -> users.id)
  └─ created_at (datetime)
```

---

## Fluxo de Requisições

Exemplos de uso dos principais endpoints:

1. **Login e obtenção de token**  
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"user@test.com","password":"pass"}'
   ```

2. **Criação de usuário**  
   ```bash
   curl -X POST http://localhost:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Alice","email":"alice@test.com","password":"123456"}'
   ```

3. **Criação de tarefa**  
   ```bash
   curl -X POST http://localhost:8000/tasks/ \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title":"Implement feature X","due_date":"2025-07-01","priority":"medium"}'
   ```

4. **Listagem de tarefas de um usuário**  
   ```bash
   curl http://localhost:8000/tasks/?assigned_to=1 \
     -H "Authorization: Bearer <TOKEN>"
   ```

---

## Tecnologias

- Python 3.10+  
- FastAPI  
- SQLAlchemy  
- Pydantic  
- passlib (bcrypt)  
- PyJWT  
- Uvicorn  
- pytest  

---

## Pré-requisitos

- Git  
- Python 3.10 ou superior  
- Ambiente virtual (venv, virtualenv ou conda)  

---

## Dependências

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic passlib[bcrypt] PyJWT pytest
```

Ou via `requirements.txt`:

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
passlib[bcrypt]
PyJWT
pytest
```

---

## Instalação

```bash
git clone https://github.com/seu-usuario/tasks-manager.git
cd tasks-manager
pip install -r requirements.txt
```

---

## Configuração e Deploy

- **Variáveis de ambiente**  
  - `JWT_SECRET`: chave secreta para tokens (padrão: `supersecret`)  
  - `DATABASE_URL`: string de conexão SQLAlchemy (padrão: `sqlite:///./app.db`)  
- **Diretório de logs**: criado automaticamente (`logs/`)  
- **Deploy**: use Uvicorn ou Docker conforme sua infraestrutura. Exemplo com Docker:
  ```dockerfile
  FROM python:3.10-slim
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
  ```

---

## Execução

```bash
python -m src.main
```
Ou:
```bash
uvicorn src.main:app --reload
```
Acesse: `http://localhost:8000/docs`

---

## Endpoints

### Autenticação

| Método | Rota           | Descrição                   |
| ------ | -------------- | --------------------------- |
| POST   | `/auth/login`  | Gera token JWT              |
| GET    | `/auth/logout` | Logout (mock)               |

### Usuários

| Método | Rota                | Descrição                      |
| ------ | ------------------- | ------------------------------ |
| POST   | `/users/`           | Cria usuário                  |
| GET    | `/users/{user_id}`  | Recupera usuário ativo        |
| PUT    | `/users/{user_id}`  | Atualiza usuário              |
| DELETE | `/users/{user_id}`  | Desativa usuário (soft delete)|

### Tarefas

| Método | Rota                        | Descrição                                    |
| ------ | --------------------------- | -------------------------------------------- |
| POST   | `/tasks/`                   | Cria nova tarefa                             |
| GET    | `/tasks/{task_id}`          | Recupera tarefa por ID                       |
| GET    | `/tasks/?assigned_to={id}`  | Lista tarefas de um usuário                  |
| PUT    | `/tasks/{task_id}`          | Atualiza tarefa                              |
| DELETE | `/tasks/{task_id}`          | Deleta tarefa                                |
| GET    | `/tasks/filter?...`         | Filtra tarefas por status, prioridade, etc.  |

### Comentários

| Método | Rota                                       | Descrição                    |
| ------ | ------------------------------------------ | ---------------------------- |
| POST   | `/tasks/{task_id}/comments`               | Adiciona comentário          |
| GET    | `/tasks/{task_id}/comments`               | Lista comentários           |
| DELETE | `/tasks/{task_id}/comments/{comment_id}`  | Remove comentário           |

---

## Logging

- Console: nível `DEBUG`  
- Arquivo (`logs/app.log`): nível `INFO`, rotação diária, 7 backups  
- Formato:
```
2025-06-18 12:34:56 | INFO     | task_controller | ...
```

---

## Banco de Dados

Por padrão SQLite (`./app.db`). Para trocar:

```bash
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
```

---

## Testes Automatizados

- **Framework**: pytest com fixtures e mocks  
- **Cobertura**: uso de `pytest --cov=src`, meta mínima de 80%  
- Testes em `tests/`, abrangendo controllers, modelos e rotas.

---

## Contribuição

1. Fork do repositório  
2. Branch feature: `git checkout -b feature/nome`  
3. Commit: `git commit -m "descrição"`  
4. Push: `git push origin feature/nome`  
5. Pull Request  

---

## Licença

MIT © Patrick Borges Wendling e Pedro Lucas Erig Gerhardt
