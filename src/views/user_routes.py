from fastapi import APIRouter, Depends
from src.controllers.user_controller import *
from src.models.user_model import UserCreate, UserUpdate, UserOut
from src.auth.jwt_utils import get_current_user
from src.models.user_model import User as UserDB
from src.controllers import utils

router = APIRouter()

@router.post("/", response_model=UserOut)
def create(user: UserCreate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return create_user(user, db)

@router.get("/{user_id}", response_model=UserOut)
def read(user_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return get_user(user_id, db)

@router.put("/{user_id}", response_model=UserOut)
def update(user_id: int, user: UserUpdate, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return update_user(user_id, user, db)

@router.delete("/{user_id}")
def delete(user_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(utils.get_db)):
    return delete_user(user_id, db)
