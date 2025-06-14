from fastapi import APIRouter, Query, Depends
from controllers.task_controller import (
    create_task, get_task, list_tasks_by_user,
    update_task, delete_task, list_tasks_filtered
)
from models.task_model import TaskCreate, TaskUpdate
from auth.jwt_utils import get_current_user
from models.user_model import User as UserDB
from datetime import date

router = APIRouter()

@router.post("/")
def create(task: TaskCreate, current_user: UserDB = Depends(get_current_user)):
    return create_task(task)

@router.get("/{task_id}")
def read(task_id: int, current_user: UserDB = Depends(get_current_user)):
    return get_task(task_id)

@router.get("/")
def list_by_user(assignedTo: int, current_user: UserDB = Depends(get_current_user)):
    return list_tasks_by_user(assignedTo)

@router.put("/{task_id}")
def update(task_id: int, task: TaskUpdate, current_user: UserDB = Depends(get_current_user)):
    return update_task(task_id, task)

@router.delete("/{task_id}")
def delete(task_id: int, current_user: UserDB = Depends(get_current_user)):
    return delete_task(task_id)

@router.get("/")
def list_by_filters(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    dueBefore: date | None = Query(None, alias="dueBefore"),
    assignedTo: int | None = Query(None, alias="assignedTo"),
    current_user: UserDB = Depends(get_current_user),
):
    return list_tasks_filtered(status, priority, dueBefore, assignedTo)