from fastapi import FastAPI
from database import Base, engine
from views import user_routes, task_routes, auth_routes

app = FastAPI(title="Gestão de Tarefas")

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
