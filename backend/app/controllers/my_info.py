from ..db import database
from fastapi import APIRouter
from ..models.users import users
from ..schemas.user import User
from ..security import authenticate
router = APIRouter()


@router.get("/my_info/")
async def my_info(api_key: str):
    """
    Gets the information of the current user:
        api_key(username+password)

    Returns an dictionary with the following information: Username, Password, Number of public images, Number 
    of private images
    """
    await authenticate(api_key)
    query = "select *  from ( select concat(username,password) as api_key,username,password,private_images,public_images from users) users where users.api_key='{api_key}'".format(
        api_key=api_key)
    result = await database.fetch_all(query=query)
    return {"Username": result[0]['username'], "Password": result[0]['password'], "Private images": result[0]['private_images'], "Public images": result[0]['public_images']}
