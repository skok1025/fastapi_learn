from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from ToDoApp.database import SessionLocal
from ToDoApp.models import Users
from passlib.context import CryptContext

from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
SECRET_KEY = "123456789"  # openssl rand -hex 32
ALGORITHM = "HS256"

# pip install passlib[bcrypt]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenUrl은 token을 발급받을 endpoint를 지정한거구요.
# 추가로 OAuth2PasswordBearer 가 각 API 요청마다 포함된 요청헤더 "Authorization" 에서 Bearer token를 가져온다고 합니다.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    # token 을 검증하는 함수이자, 정보를 가공하는 함수
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    # pip install "python-jose[cryptography]"
    # pip install python-multipart
    user = authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=20)
    )

    print(f'- created access_token: {token}')
    return {"access_token": token, "token_type": "bearer"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
