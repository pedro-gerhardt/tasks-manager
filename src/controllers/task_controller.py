from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import and_
from typing import Optional

from src.models.task_model import Task, TaskCreate, TaskUpdate
from src.models.user_model import User

import logging
logger = logging.getLogger(__name__)

# Valores válidos para status e prioridade
ALLOWED_STATUS = {"pending", "in_progress", "done"}
ALLOWED_PRIORITY = {"low", "medium", "high"}

def create_task(task: TaskCreate, db: Session):
    logger.info("create_task called with task: %s", task)
    # validações de negócio
    logger.debug("Validando prioridade: %s", task.priority)
    if task.priority not in ALLOWED_PRIORITY:
        logger.warning("Prioridade inválida: %s", task.priority)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Prioridade inválida: '{task.priority}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_PRIORITY))}."
            )
        )
    logger.debug("Validando status: %s", task.status)
    if task.status is not None and task.status not in ALLOWED_STATUS:
        logger.warning("Status inválido: %s", task.status)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Status inválido: '{task.status}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_STATUS))}."
            )
        )
    logger.debug("Validando due_date: %s", task.due_date)
    if task.due_date and task.due_date < date.today():
        logger.warning("due_date anterior: %s", task.due_date)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date não pode ser anterior à data atual."
        )

    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info("Tarefa criada com sucesso: ID=%s", db_task.id)
    return db_task

def get_task(task_id: int, db: Session):
    logger.info("get_task called for ID: %s", task_id)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Tarefa não encontrada: ID=%s", task_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )
    logger.debug("Tarefa recuperada com sucesso: ID=%s", task_id)
    return task

def list_tasks_by_user(user_id: int, db: Session):
    logger.info("list_tasks_by_user called for user ID: %s", user_id)
    # valida existência do usuário antes de listar tarefas
    user = db.query(User).filter(User.id == user_id, User.is_active).first()
    if not user:
        logger.warning("Usuário não encontrado para listagem de tarefas: ID=%s", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário (ID={user_id}) não encontrado."
        )
    tasks = db.query(Task).filter(Task.assigned_to == user_id).all()
    logger.debug("Total de tarefas retornadas para usuário %s: %d", user_id, len(tasks))
    return tasks

def update_task(task_id: int, data: TaskUpdate, db: Session):
    logger.info("update_task called for ID: %s with data: %s", task_id, data)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Tarefa não encontrada para atualização: ID=%s", task_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )

    payload = data.model_dump(exclude_unset=True)

    # validações de negócio
    if "priority" in payload:
        logger.debug("Validando prioridade no payload de update: %s", payload["priority"])
        if payload["priority"] not in ALLOWED_PRIORITY:
            logger.warning("Prioridade inválida no update: %s", payload["priority"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Prioridade inválida: '{payload['priority']}'. "
                    f"Use um dos valores: {', '.join(sorted(ALLOWED_PRIORITY))}."
                )
            )
    if "status" in payload:
        logger.debug("Validando status no payload de update: %s", payload["status"])
        if payload["status"] not in ALLOWED_STATUS:
            logger.warning("Status inválido no update: %s", payload["status"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Status inválido: '{payload['status']}'. "
                    f"Use um dos valores: {', '.join(sorted(ALLOWED_STATUS))}."
                )
            )
    if "due_date" in payload:
        logger.debug("Validando due_date no payload de update: %s", payload["due_date"])
        if payload["due_date"] < date.today():
            logger.warning("due_date inválido no update: %s", payload["due_date"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="due_date não pode ser anterior à data atual."
            )
    if "assigned_to" in payload:
        logger.debug("Validando assigned_to no payload de update: %s", payload["assigned_to"])
        assigned_id = payload["assigned_to"]
        user = db.query(User).filter(User.id == assigned_id, User.is_active).first()
        if not user:
            logger.warning("Usuário responsável não encontrado no update: ID=%s", assigned_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário responsável (ID={assigned_id}) não encontrado."
            )

    for attr, value in payload.items():
        setattr(task, attr, value)

    db.commit()
    db.refresh(task)
    logger.info("Tarefa atualizada com sucesso: ID=%s", task_id)
    return task

def delete_task(task_id: int, db: Session):
    logger.info("delete_task called for ID: %s", task_id)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Tarefa não encontrada para deleção: ID=%s", task_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )
    db.delete(task)
    db.commit()
    logger.info("Tarefa removida com sucesso: ID=%s", task_id)
    return {"message": "Tarefa removida com sucesso"}

def list_tasks_filtered(
    db: Session,
    status_filter: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[date] = None,
    user_id: Optional[int] = None,
):
    logger.info(
        "list_tasks_filtered called with "
        "status_filter=%s, priority=%s, due_before=%s, user_id=%s",
        status_filter, priority, due_before, user_id
    )
    # validação de query params
    if priority is not None and priority not in ALLOWED_PRIORITY:
        logger.warning("Prioridade inválida no filtro: %s", priority)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Prioridade inválida: '{priority}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_PRIORITY))}."
            )
        )
    if status_filter is not None and status_filter not in ALLOWED_STATUS:
        logger.warning("Status inválido no filtro: %s", status_filter)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Status inválido: '{status_filter}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_STATUS))}."
            )
        )
    query = db.query(Task)
    filters = []
    if status_filter:
        filters.append(Task.status == status_filter)
    if priority:
        filters.append(Task.priority == priority)
    if due_before:
        filters.append(Task.due_date != None)
        filters.append(Task.due_date < due_before)
    if user_id:
        filters.append(Task.assigned_to == user_id)

    if filters:
        query = query.filter(and_(*filters))

    result = query.order_by(Task.due_date).all()
    logger.debug("Total de tarefas após filtros: %d", len(result))
    return result
