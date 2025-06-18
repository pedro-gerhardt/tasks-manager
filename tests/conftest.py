import os
import pytest
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.database import Base, engine, SessionLocal
from src.models.user_model import UserCreate, User
from src.controllers.user_controller import create_user

# copia a mesma key usada em auth_controller.py
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # recria o esquema uma única vez antes de todos os testes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db() -> Session:
    # sessão limpa para cada teste
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(autouse=True, scope="function")
def clear_and_seed_db(db):
    # 1) limpa todas as tabelas
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    # 2) cria o usuário padrão: ID=1, senha “1234”
    default = UserCreate(
        name="Test User",
        email="testuser@example.com",
        password="1234"
    )
    create_user(default, db)  # já faz bcrypt.hash internamente :contentReference[oaicite:0]{index=0}
    db.commit()
    yield

@pytest.fixture(scope="function")
def create_test_user(db):
    # simplesmente retorna o usuário padrão já seedado (ID=1)
    return db.query(User).filter(User.email == "testuser@example.com").first()

@pytest.fixture(scope="function")
def auth_token(create_test_user):
    # token válido para sub=create_test_user.id
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {"sub": str(create_test_user.id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture(scope="function")
def client():
    return TestClient(app)
