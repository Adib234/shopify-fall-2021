import _pickle as cPickle
import binascii
from enum import Enum
from typing import List, Optional

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Query,
                     UploadFile)
from pydantic import BaseModel, Field

import psycopg2
from sqlalchemy.sql import func

from ..db import database
from ..request import request_user
from ..security import authenticate

router = APIRouter()


@router.post("/add/")
async def add_images(api_key: str, t: List[str] = Query(..., alias="texts", title="Description for images"),
                     c: List[str] = Query(..., alias="characteristics",
                                          title="Tags for images"),
                     p: List[str] = Query(
                         'public', alias="permissions", title="Permissions of images"),
                     images_upload: List[UploadFile] = File(...)):
    # Test this
    if (len(t) != len(c) or len(c) != len(p) or len(p) != len(images_upload)):
        raise HTTPException(
            status_code=400,
            detail="Please make sure the number of images match with your specified image properties",
        )

    await authenticate(api_key)
    result = await request_user("api_key, username, id", api_key)
    image_array = []
    for image in images_upload:
        contents = await image.read()
        image_array.append(contents)
    # add image validation

    for (permission, text, characteristics, image) in zip(p, c, t, image_array):

        query = ("insert into images(permissions,text,characteristics,date_created,user_id,img)"
                 f"values('{permission}','{text}',"
                 f"'{characteristics}'"
                 f",{func.now()},{result[0]['id']}"
                 f",'{psycopg2.Binary(image)}')")
        print(query[0:200])
        await database.execute(query=query)

    # Next update the current user
    return
