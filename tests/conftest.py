import pytest
from datetime import datetime, timedelta
import jwt
import os
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from src.models import user_model, task_model, comment_model
# from passlib.hash import bcrypt

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def db() -> Session:
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def create_test_user(db):
    # cria um usuário e autentica
    db_user = user_model.User(name="tester", email="tester@tester.com", password="1234")
    db.add
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@pytest.fixture(scope="session")
def auth_token(create_test_user, db):
    payload = {
        "sub": str(create_test_user.id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
