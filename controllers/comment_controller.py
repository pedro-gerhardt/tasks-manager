from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.comment_model import Comment, CommentCreate
from controllers.utils import get_db

def create_comment(task_id: int, user_id: int, comment_data: CommentCreate):
    db: Session = next(get_db())
    comment = Comment(
        content=comment_data.content,
        task_id=task_id,
        user_id=user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comments(task_id: int):
    db: Session = next(get_db())
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()

def delete_comment(comment_id: int, user_id: int):
    db: Session = next(get_db())
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
