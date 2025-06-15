from fastapi import APIRouter
from src.controllers.auth_controller import login_user, logout_user
from src.models.user_model import UserLogin

router = APIRouter()

@router.post("/login")
def login(credentials: UserLogin):
    return login_user(credentials)

@router.post("/logout")
def logout():
    return logout_user()
