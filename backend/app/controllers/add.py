import uuid
from enum import Enum
from typing import List, Optional

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Query,
                     UploadFile)
from pydantic import BaseModel, Field

import aiofiles
from sqlalchemy.sql import func

from ..aws import s3_resource
from ..db import database
from ..request import request_user
from ..security import authenticate

router = APIRouter()

# Maybe have a public and private route


@router.post("/add/")
async def add_images(api_key: str, t: List[str] = Query(..., alias="texts", title="Description for images"),
                     c: List[str] = Query(..., alias="characteristics",
                                          title="Tags for images"),
                     p: List[str] = Query(
                         'public', alias="permissions", title="Permissions of images"),
                     images_upload: List[UploadFile] = File(...)):
    # Test that each file uploaded is an image
    # Test this
    if (len(t) != len(c) or len(c) != len(p) or len(p) != len(images_upload)):
        raise HTTPException(
            status_code=400,
            detail="Please make sure the number of images match with your specified image properties",
        )

    await authenticate(api_key)
    result = await request_user("api_key, username, id", api_key)
    images_name = []
    for image in images_upload:
        # if image.content_type == 'image/png' or image.content_type == "image/jpg"
        print(image.content_type)
        #file_location = f"files/{image.filename}"
        # image.filename = str(uuid.uuid4())
        async with aiofiles.open(image.filename, 'wb') as out_file:
            content = await image.read()
            await out_file.write(content)

        destination = f"{result[0]['username']}/{image.filename}"
        s3_resource.Object('shopify-fall', destination).upload_file(
            Filename=image.filename)
        images_name.append(image.filename)
        await aiofiles.os.remove(image.filename)

    for (permission, text, characteristics, image) in zip(p, c, t, images_name):

        query = ("insert into images(permissions,text,characteristics,date_created,user_id,img_name)"
                 f"values('{permission}','{text}',"
                 f"'{characteristics}'"
                 f",{func.now()},{result[0]['id']}"
                 f",'{image}')")
        await database.execute(query=query)

    # Next update the current user
    return [x.filename for x in images_upload]
