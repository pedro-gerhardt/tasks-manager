from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.task_model import Task, TaskCreate, TaskUpdate
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_task(task: TaskCreate):
    db: Session = next(get_db())
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(task_id: int):
    db: Session = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def list_tasks_by_user(user_id: int):
    db: Session = next(get_db())
    return db.query(Task).filter(Task.assigned_to == user_id).all()

def update_task(task_id: int, data: TaskUpdate):
    db: Session = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    db.commit()
    return task

def delete_task(task_id: int):
    db: Session = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
