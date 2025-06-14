from fastapi import HTTPException
from src.models.user_model import UserLogin, User
from src.database import SessionLocal
import jwt
import os
from datetime import datetime, timedelta, UTC
from passlib.hash import bcrypt


SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")

def login_user(credentials: UserLogin):
    db = SessionLocal()
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not bcrypt.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(UTC) + timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

def logout_user():
    return {"message": "Logout successful (stateless JWT - handled client-side)"}
