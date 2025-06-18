import logging
from src.database import SessionLocal

logger = logging.getLogger(__name__)

def get_db():
    logger.debug("Abrindo sessão de DB")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug("Sessão de DB fechada")
