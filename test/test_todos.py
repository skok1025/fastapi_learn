from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ToDoApp.database import Base
from ToDoApp.main import app
from ToDoApp.routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ToDoApp.models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"id": 1, "username": "testuser", "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture()
def test_todos():
    todo = Todos(
        title="Test Todo",
        description="Test Description",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todos):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }]


def test_read_one_authenticated(test_todos):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }


def test_read_one_authenticated_notfound(test_todos):
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(test_todos):
    request_data = {
        "title": "New Todo",
        "description": "New Description",
        "priority": 5,
        "complete": False
    }

    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    db_data = db.query(Todos).filter(Todos.id == 2).first()
    assert db_data.title == request_data["title"]
    assert db_data.description == request_data["description"]
    assert db_data.priority == request_data["priority"]
    assert db_data.complete == request_data["complete"]