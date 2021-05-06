from fastapi.testclient import TestClient

from myapp.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/v1/users")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}