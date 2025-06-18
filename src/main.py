import logging.config
from fastapi import FastAPI
from sqlalchemy.orm import Session
import uvicorn

from src.database import Base, engine
from src.controllers.utils import get_db
from src.models.user_model import User
from passlib.hash import bcrypt
from src.views import user_routes, task_routes, auth_routes, comment_routes

# --- Configuração de logging com rotação de arquivos ---
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "level": "INFO",
            "filename": "logs/app.log",
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info("Configuração de logging aplicada")
# --------------------------------------------------------

app = FastAPI(title="Gestão de Tarefas")
logger.info("FastAPI app instanciada")

logger.info("Criando tabelas no banco de dados")
Base.metadata.create_all(bind=engine)

logger.info("Registrando rotas de usuário")
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
logger.info("Registrando rotas de tarefa")
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
logger.info("Registrando rotas de autenticação")
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
logger.info("Registrando rotas de comentários")
app.include_router(comment_routes.router, tags=["Comments"])

# Cria usuário inicial se não existir
db: Session = next(get_db())
if db.query(User).filter_by(email="root@root.com").count() < 1:
    logger.info("Criando usuário inicial 'root@root.com'")
    db_user = User(name="root", email="root@root.com", hashed_password=bcrypt.hash("root"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info("Usuário inicial criado: %s", db_user.email)

if __name__ == "__main__":
    logger.info("Iniciando servidor Uvicorn")
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
