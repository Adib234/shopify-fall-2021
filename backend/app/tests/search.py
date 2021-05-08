import pytest
from httpx import AsyncClient
from sqlalchemy.sql import func

from ..aws import s3_resource
from ..db import database
from ..main import app


async def search_test(image: str, filter: str, term: str, permissions: str) -> None:
    """
    first we upload to s3, take note of the s3 name
    then we update database, images table, not users as that is not important to test
    perform search
    delete in s3
    delete record in database

    The default user for this test is string, so string must exist
    """

    DESTINATION = "public" if permissions == "public" else "string"

    s3_resource.Object("shopify-fall", f"{DESTINATION}/{image}").upload_file(
        Filename=f'mock-data/{image}', ExtraArgs={
            'ServerSideEncryption': 'AES256'})

    query_insert = ("insert into images(permissions,text,characteristics,date_created,user_id,s3_name,org_name)"
                    f"values('{permissions}','{term}',"
                    f"'{term}'"
                    f",{func.now()},1"
                    f",'{image}','{image}')")
    await database.execute(query=query_insert)

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(f"search/{filter}/?term={term}")
        print(response.url)
        assert response.status_code == 200

    s3_resource.Object("shopify-fall",
                       f"{DESTINATION}/{image}").delete()

    query_delete = (f"delete from images where s3_name='{image}'")
    await database.execute(query=query_delete)

    query_search = (f"select s3_name from images where s3_name='{image}'")
    result = await database.fetch_all(query=query_search)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_characteristics_public_search():
    await database.connect()
    await search_test("test.jpg", "characteristics", "test", "public")
    await database.disconnect()


@pytest.mark.asyncio
async def test_text_private_search():
    await database.connect()
    await search_test("test.jpg", "text", "test", "private")
    await database.disconnect()
