# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL para SQLite (arquivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Para SQLite, precisa dessa flag para permitir múltiplas threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Factory de sessões
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Classe base para os models
Base = declarative_base()
