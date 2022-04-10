from fastapi.testclient import TestClient
from app.main import app
from app.models import Numbers
import pytest

client = TestClient(app)


def test_read_main():
    response = client.get("/add/{a}/{b}")
    assert response.status_code == 200
