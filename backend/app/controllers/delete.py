from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query

from ..aws import s3_resource
from ..db import database
from ..request import request_user
from ..security import authenticate

router = APIRouter()


@router.post("/")
async def delete_images(api_key: str,
                        d: List[str] = Query(..., alias="images_delete", description="A list of the filenames based"
                                             "on how they were stored in S3 which can be collected in my images endpoint")):
    """
    s3_name are preferred over org_name since they are unique identifiers and eliminate the possibility 
    of duplicate results found when we search for an image. The user may end up deleting an image based
    on the name it gave it but then realizes there were two or more images of the same name, s3_name 
    eliminates this edge case
    """
    await authenticate(api_key)
    init_result = await request_user("api_key, username, id", api_key)
    deleted = 0

    for image in d:

        query_find = (f"select * from images where s3_name='{image}' ")
        result = await database.fetch_all(query=query_find)
        print(len(result))
        if len(result) == 1:
            query_delete = (
                f"delete from images where s3_name='{image}' and user_id={init_result[0]['id']}")
            print(query_delete)
            await database.execute(query=query_delete)
            deleted += 1

            if result[0]['permissions'] == 'private':
                s3_resource.Object("shopify-fall",
                                   f"{init_result[0]['username']}/{result[0]['s3_name']}").delete()
                query_update = f"update users set private_images = private_images - 1 where id = {init_result[0]['id']}"
                await database.execute(query=query_update)
            else:
                s3_resource.Object('shopify-fall',
                                   f"public/{result[0]['s3_name']}").delete()
                query_update = f"update users set public_images = public_images - 1 where id = {init_result[0]['id']}"
                await database.execute(query=query_update)

    return {"number of deletes requested": len(d), "number of deletes successful": deleted}
