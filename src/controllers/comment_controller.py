from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.models.comment_model import Comment, CommentCreate
from src.models.task_model import Task
from src.controllers.utils import get_db

def create_comment(task_id: int, user_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    comment = Comment(content=comment_data.content, task_id=task_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comments(task_id: int, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()

def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado")
    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")
    db.delete(comment)
    db.commit()
    return {"message": "Comentário removido com sucesso"}
