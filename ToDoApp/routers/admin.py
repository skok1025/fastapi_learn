from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from ToDoApp.database import SessionLocal
from ToDoApp.models import Todos, Users
from ToDoApp.routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    print(user)
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")

    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()


@router.delete("/user/{user_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency, user_name: str):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_model = db.query(Users).filter(Users.username == user_name).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Users).filter(Users.username == user_name).delete()
    db.commit()
    return user_model
