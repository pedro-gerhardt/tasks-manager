from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from src.database import Base
from datetime import date

# SQLAlchemy Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")  # pending | in_progress | done
    priority = Column(String, default="medium")  # low | medium | high
    due_date = Column(Date, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"))

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int | None = None
    priority: str = "medium"
    due_date: date | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    assigned_to: int | None = None
    priority: str | None = None
    due_date: date | None = None
