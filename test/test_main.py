from fastapi.testclient import TestClient
from ToDoApp import main
from fastapi import status

client = TestClient(main.app)


def test_return_healthy():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "healthy"}