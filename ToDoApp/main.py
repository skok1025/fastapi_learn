import uvicorn
from fastapi import FastAPI

from ToDoApp import models
from ToDoApp.routers import auth, todos, admin, users
from ToDoApp.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
async def healthy():
    return {"message": "healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)