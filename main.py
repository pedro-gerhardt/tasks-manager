from fastapi import FastAPI
from views import user_routes, task_routes, auth_routes

app = FastAPI(title="Gestão de Tarefas")

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
