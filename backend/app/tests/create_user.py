import pytest
from httpx import AsyncClient
from ..db import database
from ..main import app
from ..schemas.user import Users

from sqlalchemy import delete


@pytest.mark.asyncio
async def test_empty_password():
    """
    Unit test for making sure one of the required fields isn't empty
    """
    # await database.connect()
    empty_password = Users(username="hello", password="")
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/create_user/", json={"username": empty_password.username, "password": empty_password.password})
    # await database.disconnect()
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validate_schema():
    """
    What happens when we have an integer instead for one of the string fields?
    """
    # await database.connect()
    validate = Users(username=1, password="")
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/create_user/", json={"username": validate.username, "password": validate.password})
    # await database.disconnect()
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_insert():
    """
    Testing to see if an insert works
    """
    await database.connect()
    valid = Users(username="testadib", password="shopify")
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/create_user/", json={"username": valid.username, "password": valid.password})

    assert response.status_code == 200
    assert response.json() == {
        "username": valid.username, "password": valid.password}
    
    await database.disconnect()



@pytest.mark.asyncio
async def test_duplicate():
    """
    Testing to see if an exception is raised when we try adding a username that already exists
    username: string
    password: string
    """
    await database.connect()
    existing_user = Users(username="testadib", password="shopify")
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/create_user/", json={"username": existing_user.username, "password": existing_user.password})
    # deleting the row we just put in so that we can reuse this test
    query_all = "select * from users"
    insert_rows = await database.fetch_all(query_all)
    before_rows = len(insert_rows)
    query_delete = "delete from users where users.username='{username}'".format(
        username=existing_user.username)
    await database.fetch_all(query_delete)
    delete_rows = await database.fetch_all(query_all)
    after_rows = len(delete_rows)
    await database.disconnect()
    assert after_rows == before_rows - 1

    assert response.status_code == 406
