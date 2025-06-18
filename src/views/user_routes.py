from fastapi import APIRouter, Depends, Path, Body, status
from sqlalchemy.orm import Session
from src.controllers.user_controller import create_user, get_user, update_user, delete_user
from src.models.user_model import UserCreate, UserUpdate, UserOut
from src.auth.jwt_utils import get_current_user
from src.controllers.utils import get_db

router = APIRouter()

@router.post(
    "/",
    summary="Criar novo usuário",
    description="Cria um novo usuário com nome, email e senha.",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Usuário criado com sucesso"},
        400: {"description": "Dados inválidos ou email já cadastrado"},
        401: {"description": "Não autenticado"},
    },
)
def create(
    user: UserCreate = Body(..., description="Dados para criação do usuário"),
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_user(user, db)

@router.get(
    "/{user_id}",
    summary="Obter usuário",
    description="Recupera um usuário ativo pelo ID.",
    response_model=UserOut,
    responses={
        200: {"description": "Usuário retornado"},
        401: {"description": "Não autenticado"},
        404: {"description": "Usuário não encontrado"},
    },
)
def read(
    user_id: int = Path(..., description="ID do usuário"),
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user(user_id, db)

@router.put(
    "/{user_id}",
    summary="Atualizar usuário",
    description="Atualiza nome, email e/ou senha de um usuário existente.",
    response_model=UserOut,
    responses={
        200: {"description": "Usuário atualizado"},
        400: {"description": "Dados inválidos ou email em uso"},
        401: {"description": "Não autenticado"},
        404: {"description": "Usuário não encontrado"},
    },
)
def update(
    user_id: int = Path(..., description="ID do usuário"),
    user: UserUpdate = Body(..., description="Campos a atualizar"),
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user(user_id, user, db)

@router.delete(
    "/{user_id}",
    summary="Desativar usuário",
    description="Marca o usuário como inativo (soft-delete).",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Usuário desativado"},
        401: {"description": "Não autenticado"},
        404: {"description": "Usuário não encontrado"},
    },
)
def delete(
    user_id: int = Path(..., description="ID do usuário"),
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_user(user_id, db)
