from fastapi import APIRouter, Depends
from src.controllers.comment_controller import create_comment, list_comments, delete_comment
from src.models.comment_model import Comment, CommentCreate
from src.auth.jwt_utils import get_current_user
from src.models.user_model import User as UserDB

router = APIRouter()

@router.post("/tasks/{task_id}/comments")
def add_comment(task_id: int, data: CommentCreate, current_user: UserDB = Depends(get_current_user)):
    return create_comment(task_id, current_user.id, data)

@router.get("/tasks/{task_id}/comments")
def get_comments(task_id: int, current_user: UserDB = Depends(get_current_user)):
    return list_comments(task_id)

@router.delete("/tasks/{task_id}/comments/{comment_id}")
def remove_comment(task_id: int, comment_id: int, current_user: UserDB = Depends(get_current_user)):
    return delete_comment(comment_id, current_user.id)
