from typing import List

import pytest
from httpx import AsyncClient
from sqlalchemy.sql import func

from ..aws import s3_resource
from ..db import database
from ..main import app


@pytest.mark.asyncio
async def test_unknown():
    """
    testing for unknown images
    requires: a username of string and password of string

    api_key = "stringstring"
    d = ["string","string"]
    """

    await database.connect()
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/delete/?api_key=stringstring&d=string&d=string")

    assert response.status_code == 200
    assert response.json() == {
        "number of deletes requested": 2,
        "number of deletes successful": 0
    }
    await database.disconnect()

# Helper function for the next two tests


async def success_delete(d: List[str], permission: str) -> None:
    """
    We first put the image into s3 then its properties to images table and then update the user who uploaded the 
    image

    Then we assert that once we deleted the image, that s3 objects has decreased by one, private_images 
    for the user has decreased by one and the record of that image no longer exists in images table
    """
    PERMISSIONS = 'private' if permission == 'private_images' else 'public'
    DESTINATION = 'string' if permission == 'private_images' else 'public'
    for image in d:
        s3_resource.Object("shopify-fall", f"{DESTINATION}/{image}").upload_file(
            Filename=f'mock-data/{image}', ExtraArgs={
                'ServerSideEncryption': 'AES256'})

    bucket = s3_resource.Bucket('shopify-fall')
    objects = [f for f in bucket.objects.filter(
        Prefix=f'{DESTINATION}/').all()]
    print(objects)
    before_delete_S3 = len(objects)
    print(before_delete_S3)

    await database.connect()
    for image in d:
        query_insert = ("insert into images(permissions,text,characteristics,date_created,user_id,s3_name,org_name)"
                        f"values('{PERMISSIONS}','string',"
                        f"'string'"
                        f",{func.now()},1"
                        f",'{image}','{image}')")
        await database.execute(query=query_insert)

    query_update = (
        f"update users set {permission}={permission} + {len(d)}, date_updated={func.now()} where id=1")
    await database.execute(query=query_update)
    query_before = f"select {permission} from users where id=1"
    result_update = await database.fetch_all(query=query_before)
    before_images = result_update[0][permission]

    params = "/delete/?api_key=stringstring"
    for image in d:
        params += f"&d={image}"
    print(params)
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(params)
    print(response.content)
    assert response.status_code == 200
    assert response.json() == {
        "number of deletes requested": len(d),
        "number of deletes successful": len(d)
    }

    objects = [f for f in bucket.objects.filter(
        Prefix=f'{DESTINATION}/').all()]
    print(objects)
    after_delete_S3 = len(objects)
    print(after_delete_S3)
    assert before_delete_S3 - len(d) == after_delete_S3

    for image in d:
        query_find = f"select * from images where s3_name='{image}'"
        result = await database.fetch_all(query=query_find)
        assert len(result) == 0

    query_after = f"select {permission} from users where id=1"
    result_update = await database.fetch_all(query_after)
    after_images = result_update[0][permission]
    print(after_images)

    assert before_images - len(d) == after_images

    await database.disconnect()


@pytest.mark.asyncio
async def test_single_private():
    await success_delete(["test.jpg"], "private_images")


@pytest.mark.asyncio
async def test_bulk_public():
    await success_delete(["test.jpg", "test1.jpg"], "public_images")
