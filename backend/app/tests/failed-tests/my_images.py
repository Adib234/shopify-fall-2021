import pytest
from httpx import AsyncClient

from ..db import database
from ..main import app


def all_asserts(response):
    assert response.status_code == 200
    assert response.template.name == 'images.html'
    assert "request" in response.context


@pytest.mark.asyncio
async def test_all():
    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/my_images/all/?api_key=stringstring")
        all_asserts(response)
    await database.disconnect()


@pytest.mark.asyncio
async def test_private():
    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/my_images/private/?api_key=stringstring")
        all_asserts(response)
    await database.disconnect()


@pytest.mark.asyncio
async def test_public():
    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/my_images/public/?api_key=stringstring")
        all_asserts(response)
    await database.disconnect()
