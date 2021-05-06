from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def all_asserts(response):
    assert response.status_code == 200
    assert response.template.name == 'images.html'
    assert "request" in response.context


def test_all():
    response = client.get("http://127.0.0.1:8000/my_images/all")
    all_asserts(response)


def test_private():
    response = client.get("http://127.0.0.1:8000/my_images/private")
    all_asserts(response)


def test_public():
    response = client.get("http://127.0.0.1:8000/my_images/public")
    all_asserts(response)
