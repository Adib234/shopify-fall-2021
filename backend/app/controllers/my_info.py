from ..db import database
from fastapi import APIRouter
from ..security import authenticate
from ..request import request_user
router = APIRouter()


@router.get("/my_info/")
async def my_info(api_key: str):
    """
    Gets the information of the current user:
        api_key(username+password)

    Returns an dictionary with the following information: Username, Password, Number of public images, Number 
    of private images
    """
    await authenticate(api_key)  # We don't have to deal with exception handling since this function does this for us
    result = await request_user("api_key, username, password, private_images, public_images", api_key)
    return {"Username": result[0]['username'], "Password": result[0]['password'], "Private images": result[0]['private_images'], "Public images": result[0]['public_images']}
