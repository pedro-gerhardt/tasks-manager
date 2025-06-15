from fastapi import FastAPI
from src.database import Base, engine
from src.views import user_routes, task_routes, auth_routes, comment_routes
from sqlalchemy.orm import Session
from src.controllers.utils import get_db
from src.models.user_model import User

app = FastAPI(title="Gestão de Tarefas")

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(comment_routes.router, tags=["Comments"])

db: Session = next(get_db())
if db.query(User).filter_by(email="root@root.com").count() < 1:
    db_user = User(name="root", email="root@root.com", password="root")
    db.add
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
