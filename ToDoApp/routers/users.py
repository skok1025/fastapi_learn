from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ToDoApp.database import SessionLocal
from ToDoApp.models import Users
from ToDoApp.routers.auth import get_current_user, bcrypt_context
from starlette import status

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return db.query(Users).filter(Users.id == user.get('id')).first()


class PasswordRequest(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, password_request: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # 현재 password 검증
    if not bcrypt_context.verify(password_request.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
    db.commit()