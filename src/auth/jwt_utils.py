import os
import logging
import jwt
from datetime import datetime, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.models.user_model import User
from src.controllers.utils import get_db

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    logger.debug("Decodificando JWT token")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (jwt.PyJWTError, ValueError):
        logger.warning("Token inválido ou expirado")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        logger.warning("Token válido mas usuário não encontrado ou inativo: ID=%d", user_id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado")
    logger.debug("Token válido para usuário ID=%d", user_id)
    return user
