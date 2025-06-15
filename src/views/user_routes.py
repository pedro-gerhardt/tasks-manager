from fastapi import APIRouter, Depends
from src.controllers.user_controller import *
from src.models.user_model import UserCreate, UserUpdate, UserOut
from src.auth.jwt_utils import get_current_user
from src.models.user_model import User as UserDB

router = APIRouter()

@router.post("/", response_model=UserOut)
def create(user: UserCreate, current_user: UserDB = Depends(get_current_user)):
    return create_user(user)

@router.get("/{user_id}", response_model=UserOut)
def read(user_id: int, current_user: UserDB = Depends(get_current_user)):
    return get_user(user_id)

@router.put("/{user_id}", response_model=UserOut)
def update(user_id: int, user: UserUpdate, current_user: UserDB = Depends(get_current_user)):
    return update_user(user_id, user)

@router.delete("/{user_id}")
def delete(user_id: int, current_user: UserDB = Depends(get_current_user)):
    return delete_user(user_id)
