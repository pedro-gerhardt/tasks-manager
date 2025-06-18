from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.database import Base

# SQLAlchemy Model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

# Pydantic Schemas
class CommentCreate(BaseModel):
    content: str = Field(
        ...,
        description="Texto do comentário a ser adicionado à tarefa",
        min_length=1,
        max_length=500,
        example="Precisamos revisar esse ponto de integração."
    )

class CommentOut(BaseModel):
    id: int = Field(..., description="Identificador único do comentário")
    created_at: datetime = Field(..., description="Data e hora de criação do comentário")
    content: str = Field(..., description="Texto completo do comentário")

    model_config = ConfigDict(from_attributes=True)

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(
        None,
        description="Novo texto para o comentário",
        min_length=1,
        max_length=500,
        example="Atualizando o texto do comentário."
    )
