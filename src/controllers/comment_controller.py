import logging
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.models.comment_model import Comment, CommentCreate
from src.models.task_model import Task
from src.controllers.utils import get_db

logger = logging.getLogger(__name__)

def create_comment(task_id: int, user_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    logger.info("Criando comentário na tarefa ID=%d por usuário ID=%d", task_id, user_id)
    if not db.query(Task).filter(Task.id == task_id).first():
        logger.warning("Tarefa não encontrada para comentário ID=%d", task_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    comment = Comment(content=comment_data.content, task_id=task_id, user_id=user_id)
    db.add(comment)
    db.commit()
    logger.info("Comentário criado ID=%d na tarefa ID=%d", comment.id, task_id)
    db.refresh(comment)
    return comment

def list_comments(task_id: int, db: Session = Depends(get_db)):
    logger.info("Listando comentários para tarefa ID=%d", task_id)
    if not db.query(Task).filter(Task.id == task_id).first():
        logger.warning("Tarefa não encontrada para listagem de comentários ID=%d", task_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    comments = db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()
    logger.debug("Total de comentários retornados: %d", len(comments))
    return comments

def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    logger.info("Removendo comentário ID=%d por usuário ID=%d", comment_id, user_id)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning("Comentário não encontrado: ID=%d", comment_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado")
    if comment.user_id != user_id:
        logger.warning("Permissão negada para deleção de comentário ID=%d pelo usuário ID=%d", comment_id, user_id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")
    db.delete(comment)
    db.commit()
    logger.info("Comentário removido com sucesso ID=%d", comment_id)
    return {"message": "Comentário removido com sucesso"}
