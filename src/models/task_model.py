from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from src.database import Base

# SQLAlchemy Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")   # pending | in_progress | done
    priority = Column(String, default="medium")  # low | medium | high
    due_date = Column(Date, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"))

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        description="Título da tarefa",
        min_length=1,
        max_length=200,
        example="Implementar autenticação JWT"
    )
    description: Optional[str] = Field(
        None,
        description="Descrição detalhada da tarefa",
        example="Adicionar endpoints de login e logout"
    )
    assigned_to: Optional[int] = Field(
        None,
        description="ID do usuário responsável pela tarefa",
        example=1
    )
    status: Optional[str] = Field(
        None,
        description="Status inicial (pending|in_progress|done)",
        example="pending"
    )
    priority: str = Field(
        "medium",
        description="Prioridade da tarefa (low|medium|high)",
        example="high"
    )
    due_date: Optional[date] = Field(
        None,
        description="Data limite para conclusão (YYYY-MM-DD)",
        example="2025-06-30"
    )

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        description="Novo título da tarefa",
        min_length=1,
        max_length=200
    )
    description: Optional[str] = Field(
        None,
        description="Nova descrição da tarefa"
    )
    status: Optional[str] = Field(
        None,
        description="Novo status (pending|in_progress|done)",
        example="in_progress"
    )
    assigned_to: Optional[int] = Field(
        None,
        description="Novo responsável pela tarefa"
    )
    priority: Optional[str] = Field(
        None,
        description="Nova prioridade (low|medium|high)",
        example="low"
    )
    due_date: Optional[date] = Field(
        None,
        description="Nova data de vencimento"
    )

class TaskOut(BaseModel):
    id: int = Field(..., description="Identificador único da tarefa")
    title: str = Field(..., description="Título da tarefa")
    description: Optional[str] = Field(None, description="Descrição detalhada da tarefa")
    status: str = Field(..., description="Estado atual da tarefa")
    priority: str = Field(..., description="Prioridade da tarefa")
    due_date: Optional[date] = Field(None, description="Data limite para conclusão")
    assigned_to: Optional[int] = Field(None, description="ID do usuário responsável pela tarefa")

    model_config = ConfigDict(from_attributes=True)
