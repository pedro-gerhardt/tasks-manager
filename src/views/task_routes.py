from fastapi import APIRouter, Depends, Path, Body, Query, status
from datetime import date
from typing import List
from sqlalchemy.orm import Session
from src.controllers.task_controller import (
    create_task, get_task, update_task, delete_task, list_tasks_filtered, list_tasks_by_user
)
from src.models.task_model import TaskCreate, TaskUpdate, TaskOut
from src.auth.jwt_utils import get_current_user
from src.controllers.utils import get_db

router = APIRouter()

@router.post(
    "/",
    summary="Criar tarefa",
    description="Cria uma nova tarefa opcionalmente atribuída a um usuário.",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Tarefa criada com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autenticado"},
    },
)
def create(
    task: TaskCreate = Body(..., description="Dados para criação da tarefa"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_task(task, db)

@router.get(
    "/{task_id}",
    summary="Obter tarefa",
    description="Recupera uma tarefa pelo seu ID.",
    response_model=TaskOut,
    responses={
        200: {"description": "Tarefa retornada"},
        401: {"description": "Não autenticado"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def read(
    task_id: int = Path(..., description="ID da tarefa"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_task(task_id, db)

@router.put(
    "/{task_id}",
    summary="Atualizar tarefa",
    description="Atualiza dados de uma tarefa existente.",
    response_model=TaskOut,
    responses={
        200: {"description": "Tarefa atualizada com sucesso"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autenticado"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def update(
    task_id: int = Path(..., description="ID da tarefa"),
    task: TaskUpdate = Body(..., description="Campos a atualizar"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_task(task_id, task, db)

@router.delete(
    "/{task_id}",
    summary="Remover tarefa",
    description="Remove uma tarefa pelo seu ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Tarefa removida com sucesso"},
        401: {"description": "Não autenticado"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def delete(
    task_id: int = Path(..., description="ID da tarefa"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_task(task_id, db)

@router.get(
    "/",
    summary="Listar tarefas com filtros",
    description="Filtra tarefas por status, prioridade, data ou usuário responsável.",
    response_model=List[TaskOut],
    responses={200: {"description": "Lista retornada com sucesso"}, 401: {"description": "Não autenticado"}},
)
def list_filtered(
    status: str | None = Query(None, description="Status da tarefa"),
    priority: str | None = Query(None, description="Prioridade da tarefa"),
    due_before: date | None = Query(None, alias="dueBefore", description="Data limite YYYY-MM-DD"),
    user_id: int | None = Query(None, alias="assignedTo", description="ID do usuário responsável"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_tasks_filtered(db, status, priority, due_before, user_id)

@router.get(
    "/user/{user_id}",
    summary="Listar tarefas por usuário",
    description="Retorna todas as tarefas atribuídas a um usuário.",
    response_model=List[TaskOut],
    responses={200: {"description": "Lista retornada com sucesso"}, 401: {"description": "Não autenticado"}},
)
def list_by_user(
    user_id: int = Path(..., description="ID do usuário"),
    current_user: TaskOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_tasks_by_user(user_id, db)
