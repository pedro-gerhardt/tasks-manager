from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from src.controllers.auth_controller import login_user, logout_user
from src.controllers.utils import get_db
from src.models.user_model import UserLogin

router = APIRouter()

class TokenOut(BaseModel):
    access_token: str = Field(..., description="JWT de acesso")
    token_type: str = Field(..., description="Tipo de token (bearer)")

class MessageOut(BaseModel):
    message: str = Field(..., description="Mensagem de resposta")

@router.post(
    "/login",
    summary="Autenticar usuário",
    description="Valida credenciais e retorna token JWT.",
    response_model=TokenOut,
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Autenticado"}, 401: {"description": "Credenciais inválidas"}},
)
def login(
    credentials: UserLogin = Body(..., description="Email e senha para login"),
    db: Session = Depends(get_db),
):
    return login_user(credentials, db)

@router.post(
    "/logout",
    summary="Deslogar usuário",
    description="Operação stateless: descarta token localmente.",
    response_model=MessageOut,
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Logout realizado com sucesso"}},
)
def logout():
    return logout_user()
