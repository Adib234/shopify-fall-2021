import os
import uuid
from enum import Enum
from typing import List, Optional, Union

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Query,
                     UploadFile)
from pydantic import BaseModel, Field

import aiofiles
import boto3
from sqlalchemy.sql import func

from ..aws import s3_resource
from ..db import database
from ..request import request_user
from ..security import authenticate

router = APIRouter()


async def add_images(permission: str, api_key: str, t: List[str], images_upload: List[UploadFile] = File(...)):

    # Test that each file uploaded is an image
    # Test this
    if (len(t) != len(images_upload)):
        raise HTTPException(
            status_code=400,
            detail="Please make sure the number of images match with your specified image properties",
        )

    await authenticate(api_key)
    result = await request_user(f"api_key, username, id, {permission}_images", api_key)
    s3_properties = []
    org_name = []
    # For each image, upload it to S3
    for image in images_upload:
        if image.content_type == 'image/png' or image.content_type == "image/jpeg":

            org_name.append(image.filename)
            image.filename = f"{str(uuid.uuid4())}.{image.content_type.split('/')[1]}"
            async with aiofiles.open(image.filename, 'wb') as out_file:
                content = await image.read()
                await out_file.write(content)

            directory = 'public' if permission == 'public' else result[0]['username']
            destination = f"{directory}/{image.filename}"
            # We are encrypting our data using Amazon's AES-256 server-side encryption algorithm
            s3_resource.Object('shopify-fall', destination).upload_file(
                Filename=image.filename, ExtraArgs={
                    'ServerSideEncryption': 'AES256'})

            # classifying the image using AWS Rekognition
            client = boto3.client('rekognition',
                                  aws_access_key_id=os.environ.get(
                                      "AWS_SERVER_PUBLIC_KEY"),
                                  aws_secret_access_key=os.environ.get(
                                      "AWS_SERVER_SECRET_KEY"),
                                  region_name=os.environ.get("REGION_NAME"))
            classify = client.detect_labels(
                Image={'S3Object': {'Bucket': 'shopify-fall', 'Name': destination}}, MinConfidence=75)
            characteristics = [c['Name'] for c in classify['Labels']]

            s3_properties.append({"s3_name": image.filename,
                                  "characteristics": characteristics})
            await aiofiles.os.remove(image.filename)
        else:
            raise HTTPException(
                status_code=400,
                detail="Please make sure that your images have any extension of the following: png, jpeg",
            )

    # Enter the new image and properties into the database
    for (text, s3, org) in zip(t, s3_properties, org_name):

        s3_name, characteristics = s3["s3_name"], ' '.join(
            s3["characteristics"])
        print(characteristics)
        query_insert = ("insert into images(permissions,text,characteristics,date_created,user_id,s3_name,org_name)"
                        f"values('{permission}','{text}',"
                        f"'{characteristics}'"
                        f",{func.now()},{result[0]['id']}"
                        f",'{s3_name}','{org}')")
        await database.execute(query=query_insert)

    # Next update the current user
    total_images = result[0][f'{permission}_images'] + len(s3_properties)
    print(total_images)
    query_update = (
        f"update users set {permission}_images={total_images}, date_updated={func.now()} where id={result[0]['id']}")
    await database.execute(query=query_update)

    return {"images_uploaded": [x.filename for x in images_upload], f"total_{permission}": total_images}

# Both routes are dependent on the helper function above


@router.post("/private/")
async def add_images_private(api_key: str, texts: List[str] = Query(..., alias="t", description="Description for images"),
                             images_upload: List[UploadFile] = File(...)):
    """
    If successful will return the image name and total private images that the user has
    """
    result = await add_images('private', api_key, texts, images_upload)
    return result


@router.post("/public/")
async def add_images_public(api_key: str, texts: List[str] = Query(..., alias="t", description="Description for images"),
                            images_upload: List[UploadFile] = File(...)):
    """
    If successful will return the image name and total public images that the user has
    """
    result = await add_images('public', api_key, texts, images_upload)
    return result
