from fastapi import APIRouter, UploadFile, File, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from ..models import PermissionsEnum
from ..security import authenticate
from ..request import request_user
from sqlalchemy.sql import func
from ..db import database
router = APIRouter()


class ImagesProperty(BaseModel):

    text: str = Field(max_length=256)
    characteristics: str = Field(max_length=256)
    permissions: Optional[PermissionsEnum] = Field(PermissionsEnum.public)
    api_key: str

    class Config:
        arbitrary_types_allowed = True


@router.post("/add/")
async def add_images(images: List[UploadFile] = File(...), images_property: ImagesProperty = Depends()):
    await authenticate(images_property.api_key)
    result = await request_user("api_key, username, id", images_property.api_key)
    query = ("insert into images(permissions,text,characteristics,date_created,user_id)"
             f"values('{images_property.permissions.value}','{images_property.text}',"
             f"'{images_property.characteristics}'"
             f",{func.now()},{result[0]['id']})")
    await database.execute(query=query)

    # Next update the current user
    return {"filenames": [file.filename for file in images]}
