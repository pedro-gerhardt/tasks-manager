from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")  # pending | in_progress | done
    assigned_to = Column(Integer, ForeignKey("users.id"))

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    assigned_to: int | None = None
