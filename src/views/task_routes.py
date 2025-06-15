from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from src.controllers.task_controller import (
    create_task, get_task, list_tasks_by_user,
    update_task, delete_task, list_tasks_filtered
)
from src.models.task_model import TaskCreate, TaskUpdate, TaskOut
from src.auth.jwt_utils import get_current_user
from src.models.user_model import User as UserDB
from datetime import date
from src.controllers import utils

router = APIRouter()

@router.post("/", response_model=TaskOut)
def create(task: TaskCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return create_task(task, db)

@router.get("/{task_id}", response_model=TaskOut)
def read(task_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return get_task(task_id, db)

@router.get("/", response_model=list[TaskOut])
def list_by_user(assignedTo: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return list_tasks_by_user(assignedTo, db)

@router.put("/{task_id}", response_model=TaskOut)
def update(task_id: int, task: TaskUpdate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return update_task(task_id, task, db)

@router.delete("/{task_id}")
def delete(task_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return delete_task(task_id, db)

@router.get("/", response_model=list[TaskOut])
def list_by_filters(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    dueBefore: date | None = Query(None, alias="dueBefore"),
    assignedTo: int | None = Query(None, alias="assignedTo"),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(utils.get_db)
):
    return list_tasks_filtered(db, status, priority, dueBefore, assignedTo)