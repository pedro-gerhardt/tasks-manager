import logging
from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from src.models.user_model import User, UserCreate, UserUpdate
from src.controllers.utils import get_db

logger = logging.getLogger(__name__)

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Tentando criar usuário email=%s", user.email)
    if db.query(User).filter(User.email == user.email).first():
        logger.warning("Email já existente: %s", user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    hashed_pw = bcrypt.hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    try:
        db.commit()
        logger.info("Usuário criado com ID=%d", db_user.id)
    except IntegrityError:
        db.rollback()
        logger.error("Erro de integridade ao criar usuário: email=%s", user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falha ao criar usuário")
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info("Recuperando usuário ID=%d", user_id)
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        logger.warning("Usuário não encontrado: ID=%d", user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    logger.info("Atualizando usuário ID=%d", user_id)
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        logger.warning("Tentativa de atualização de usuário inválido/inativo: ID=%d", user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if data.name:
        user.name = data.name
    if data.email:
        if db.query(User).filter(User.email == data.email, User.id != user_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já em uso")
        user.email = data.email
    if data.password:
        logger.info("Atualizando senha do usuário ID=%d", user_id)
        user.hashed_password = bcrypt.hash(data.password)
    db.commit()
    logger.info("Usuário atualizado: ID=%d", user_id)
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info("Deletando usuário ID=%d", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning("Usuário não encontrado para deleção: ID=%d", user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    user.is_active = False
    db.commit()
    logger.info("Usuário desativado (soft-delete): ID=%d", user_id)
    return {"message": "Usuário desativado com sucesso"}
