from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.user_model import User, UserCreate, UserUpdate
from src.controllers.utils import get_db

def create_user(user: UserCreate):
    db: Session = next(get_db())
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(user_id: int, data: UserUpdate):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    if data.password:
        user.password = data.password
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": "User deactivated"}
