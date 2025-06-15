from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.task_model import Task, TaskCreate, TaskUpdate
from src.controllers.utils import get_db
from typing import Optional
from datetime import date
from sqlalchemy import and_


def create_task(task: TaskCreate, db: Session):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def list_tasks_by_user(user_id: int, db: Session):
    return db.query(Task).filter(Task.assigned_to == user_id).all()

def update_task(task_id: int, data: TaskUpdate, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for attr, value in data.model_dump(exclude_unset=True).items():
        setattr(task, attr, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

def list_tasks_filtered(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[date] = None,
    user_id: Optional[int] = None,
):
    query = db.query(Task)

    filters = []

    if status:
        filters.append(Task.status == status)
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