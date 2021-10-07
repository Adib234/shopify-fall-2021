from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..aws import s3_resource
from ..db import database
from ..request import request_user
from ..security import authenticate

templates = Jinja2Templates(
    directory="/Users/admin/shopify-fall-2021/backend/app/templates")
router = APIRouter()

bucket = s3_resource.Bucket('shopify-fall')


async def get_images(repository: str, result):
    # result is a postgresql record
    print(repository)
    objects = [(f"https://shopify-fall.s3.us-east-2.amazonaws.com/{f.key}", f.key) for f in bucket.objects.filter(
        Prefix=f"{repository}/").all()]
    print(objects)

    all_images = []
    for image in objects:
        url, s3_name = image
        # Gets the properties of the image and makes sure that user has access control
        query_fetch = f"select * from images where s3_name='{s3_name.split('/')[1]}' and user_id={result[0]['id']}"
        print("hello", query_fetch)
        result_fetch = await database.fetch_all(query=query_fetch)
        print(result_fetch[0])
        all_images.append({"s3_name": s3_name.split(
            '/')[1], "url": url, "org_name": result_fetch[0]["org_name"],
            "permission": result_fetch[0]["permissions"],
            "date_created": result_fetch[0]["date_created"]})

    return all_images

"""
The following routes returns all the images that the user has access control based on the repository
over as HTML so that they can see their images and its' properties
"""


@router.get("/all/", response_class=HTMLResponse)
async def all_images(api_key: str, request: Request):

    await authenticate(api_key)
    result = await request_user(f"api_key, username, id", api_key)

    private_images = await get_images(result[0]['username'], result)
    public_images = await get_images('public', result)

    return templates.TemplateResponse("images.html", {"request": request, "all_images": private_images + public_images, "user": result[0]['username']})


@router.get("/private/", response_class=HTMLResponse)
async def private_images(api_key: str, request: Request):
    await authenticate(api_key)
    result = await request_user(f"api_key, username, id", api_key)

    private_images = await get_images(result[0]['username'], result)
    return templates.TemplateResponse("images.html", {"request": request, "all_images": private_images, "user": result[0]['username']})


@router.get("/public/", response_class=HTMLResponse)
async def public_images(api_key: str, request: Request):
    await authenticate(api_key)
    result = await request_user(f"api_key, username, id", api_key)

    public_images = await get_images('public', result)
    return templates.TemplateResponse("images.html", {"request": request, "all_images": public_images, "user": result[0]['username']})
