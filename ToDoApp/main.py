import uvicorn
from fastapi import FastAPI

from ToDoApp import models
from ToDoApp.routers import auth, todos
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)