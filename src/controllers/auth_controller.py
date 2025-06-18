import os
from datetime import datetime, timedelta, UTC
import jwt
from fastapi import HTTPException, status, Depends
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from src.models.user_model import UserLogin, User
from src.controllers.utils import get_db  # dependency para a sessão

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2

def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    # busca o usuário pelo email
    user = db.query(User).filter(User.email == credentials.email).first()
    # compara senha em texto plano vs hash do banco
    if not user or not bcrypt.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    # gera payload e token
    expire = datetime.now(UTC) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

def logout_user():
    return {"message": "Logout realizado com sucesso"}
