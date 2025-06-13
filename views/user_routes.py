from fastapi import APIRouter, Depends
from controllers.user_controller import *
from models.user_model import UserCreate, UserUpdate
from auth.jwt_utils import get_current_user
from models.user_model import User as UserDB

router = APIRouter()

@router.post("/")
def create(user: UserCreate):
    return create_user(user)

@router.get("/{user_id}")
def read(user_id: int, current_user: UserDB = Depends(get_current_user)):
    return get_user(user_id)

@router.put("/{user_id}")
def update(user_id: int, user: UserUpdate, current_user: UserDB = Depends(get_current_user)):
    return update_user(user_id, user)

@router.delete("/{user_id}")
def delete(user_id: int, current_user: UserDB = Depends(get_current_user)):
    return delete_user(user_id)
