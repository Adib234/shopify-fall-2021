from typing import List

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..db import database

templates = Jinja2Templates(
    directory="/Users/admin/shopify-app-fall/backend/app/templates")
router = APIRouter()


async def search(column: str, search_term: str) -> List[dict]:
    if search_term[0] != '\'' and search_term[-1] != '\'':
        if search_term[0] != '\'':
            search_term = '\'' + search_term
        if search_term[-1] != '\'':
            search_term += '\''

    query_search = f"select {column},s3_name,org_name,permissions,user_id from images where to_tsvector({column}) @@ plainto_tsquery({search_term})"
    result = await database.fetch_all(query=query_search)

    final_data = []  # keys: s3_name, org_name, column, image_url

    for image in result:

        if image["permissions"] == 'public':
            final_data.append(
                {"s3_name": image["s3_name"], "org_name": image["org_name"],
                 "search_category": image[column],
                 "url": f"https://shopify-fall.s3.us-east-2.amazonaws.com/public/{image['s3_name']}"})
        else:
            find_user = f"select username,id from users where id={image['user_id']}"
            result_find = await database.fetch_all(query=find_user)
            print(
                f"https://shopify-fall.s3.us-east-2.amazonaws.com/{result_find[0]['username']}/{image['s3_name']}")
            final_data.append(
                {"s3_name": image["s3_name"], "org_name": image["org_name"],
                 "search_category": image[column],
                 "url": f"https://shopify-fall.s3.us-east-2.amazonaws.com/{result_find[0]['username']}/{image['s3_name']}"})

    return final_data


@router.get("/text/")
async def search_by_text(request: Request, term: str = Query(..., description="Text you entered for your image when you first uploaded it, enter it with single quotes"),):
    result = await search("text", term)
    return templates.TemplateResponse("search_results.html", {"request": request, "all_images": result})


@router.get("/characteristics/")
async def search_by_characteristics(request: Request, term: str = Query(...)):
    result = await search("characteristics", term)
    return templates.TemplateResponse("search_results.html", {"request": request, "all_images": result})
