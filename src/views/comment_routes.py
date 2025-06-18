from fastapi import APIRouter, Depends, Path, Body, status
from typing import List
from sqlalchemy.orm import Session
from src.controllers.comment_controller import create_comment, list_comments, delete_comment
from src.models.comment_model import CommentCreate, CommentOut, CommentUpdate
from src.auth.jwt_utils import get_current_user
from src.controllers.utils import get_db

router = APIRouter()

@router.post(
    "/tasks/{task_id}/comments",
    summary="Adicionar comentário",
    description="Cria um comentário numa tarefa específica.",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Comentário criado"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autenticado"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def add(
    task_id: int = Path(..., description="ID da tarefa"),
    data: CommentCreate = Body(..., description="Conteúdo do comentário"),
    current_user: CommentOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_comment(task_id, current_user.id, data, db)

@router.get(
    "/tasks/{task_id}/comments",
    summary="Listar comentários",
    description="Retorna todos os comentários de uma tarefa.",
    response_model=List[CommentOut],
    responses={
        200: {"description": "Lista retornada com sucesso"},
        401: {"description": "Não autenticado"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def get_all(
    task_id: int = Path(..., description="ID da tarefa"),
    current_user: CommentOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_comments(task_id, db)

@router.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    summary="Remover comentário",
    description="Remove um comentário pelo ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Comentário removido"},
        401: {"description": "Não autenticado"},
        403: {"description": "Permissão negada"},
        404: {"description": "Comentário não encontrado"},
    },
)
def remove(
    task_id: int = Path(..., description="ID da tarefa"),
    comment_id: int = Path(..., description="ID do comentário"),
    current_user: CommentOut = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_comment(comment_id, current_user.id, db)
