import pytest
from httpx import AsyncClient

from ..db import database
from ..main import app


@pytest.mark.asyncio
async def test_empty():
    """
    Unit test for making sure one of the required fields isn't empty
    """
    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/my_info/?api_key=""")
    assert response.status_code == 401
    await database.disconnect()


@pytest.mark.asyncio
async def test_valid_user():
    """
    Unit test for valid user
    username:string
    password:string
    """
    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/my_info/?api_key=stringstring")
    assert response.status_code == 200
    await database.disconnect()
