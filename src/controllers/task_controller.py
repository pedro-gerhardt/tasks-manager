from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import and_
from typing import Optional

from src.models.task_model import Task, TaskCreate, TaskUpdate
from src.models.user_model import User

# Valores válidos para status e prioridade
ALLOWED_STATUS = {"pending", "in_progress", "done"}
ALLOWED_PRIORITY = {"low", "medium", "high"}

def create_task(task: TaskCreate, db: Session):
    # validações de negócio
    if task.priority not in ALLOWED_PRIORITY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Prioridade inválida: '{task.priority}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_PRIORITY))}."
            )
        )
    if task.status is not None and task.status not in ALLOWED_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Status inválido: '{task.status}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_STATUS))}."
            )
        )
    if task.assigned_to is not None:
        user = db.query(User).filter(User.id == task.assigned_to, User.is_active).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário responsável (ID={task.assigned_to}) não encontrado."
            )
    if task.due_date and task.due_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date não pode ser anterior à data atual."
        )

    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )
    return task


def list_tasks_by_user(user_id: int, db: Session):
    # valida existência do usuário antes de listar tarefas
    user = db.query(User).filter(User.id == user_id, User.is_active).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário (ID={user_id}) não encontrado."
        )
    return db.query(Task).filter(Task.assigned_to == user_id).all()


def update_task(task_id: int, data: TaskUpdate, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )

    payload = data.model_dump(exclude_unset=True)

    # validações de negócio
    if "priority" in payload and payload["priority"] not in ALLOWED_PRIORITY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Prioridade inválida: '{payload['priority']}'. "
                f"Use: {', '.join(sorted(ALLOWED_PRIORITY))}."
            )
        )
    if "status" in payload and payload["status"] not in ALLOWED_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Status inválido: '{payload['status']}'. "
                f"Use: {', '.join(sorted(ALLOWED_STATUS))}."
            )
        )
    if "assigned_to" in payload:
        assigned_id = payload["assigned_to"]
        if assigned_id is not None:
            user = db.query(User).filter(User.id == assigned_id, User.is_active).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuário responsável (ID={assigned_id}) não encontrado."
                )
    if "due_date" in payload and payload["due_date"] < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="due_date não pode ser anterior à data atual."
        )

    for attr, value in payload.items():
        setattr(task, attr, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa (ID={task_id}) não encontrada."
        )
    db.delete(task)
    db.commit()
    return {"message": "Tarefa removida com sucesso"}


def list_tasks_filtered(
    db: Session,
    status_filter: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[date] = None,
    user_id: Optional[int] = None,
):
    # validação de query params
    if priority is not None and priority not in ALLOWED_PRIORITY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Prioridade inválida: '{priority}'. "
                f"Use um dos valores: {', '.join(sorted(ALLOWED_PRIORITY))}."
            )
        )
    if status_filter is not None and status_filter not in ALLOWED_STATUS:
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

    return query.order_by(Task.due_date).all()