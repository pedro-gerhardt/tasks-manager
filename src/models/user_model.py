from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str = Field(
        ...,
        description="Nome completo do usuário",
        min_length=1,
        max_length=100,
        example="Patrick Wendling"
    )
    email: EmailStr = Field(
        ...,
        description="Endereço de email único e válido",
        example="patrick@example.com"
    )
    password: str = Field(
        ...,
        description="Senha do usuário (mínimo 4 caracteres)",
        min_length=4,
        example="strongP@ssw0rd"
    )

class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email cadastrado do usuário",
        example="patrick@example.com"
    )
    password: str = Field(
        ...,
        description="Senha do usuário",
        min_length=4,
        example="strongP@ssw0rd"
    )

class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Novo nome completo do usuário",
        min_length=1,
        max_length=100,
        example="Patrick Wendling"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Novo email do usuário",
        example="novo@example.com"
    )
    password: Optional[str] = Field(
        None,
        description="Nova senha do usuário (mínimo 4 caracteres)",
        min_length=4,
        example="newP@ssw0rd"
    )

class UserOut(BaseModel):
    id: int = Field(..., description="Identificador único do usuário")
    name: str = Field(..., description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Endereço de email do usuário")
    is_active: bool = Field(..., description="Indica se o usuário está ativo no sistema")

    model_config = ConfigDict(from_attributes=True)
