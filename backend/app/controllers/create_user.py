from ..schemas.user import Users
from ..db import database
from ..models import User
from fastapi import HTTPException, APIRouter

router = APIRouter()


@router.post("/create_user/")
async def create_user(user: Users):
    """
    Create a user with all the information:
    :param user: User input.
        - **username**: username to access their private repositories (required)
        - **password**: password to access their private repositories (required)
    Returns the values that they entered (username, password)
    """
    duplicate = False

    if user.username == '' or user.password == '':
        raise HTTPException(
            status_code=404, detail="Please fill out a password or username")

    query = "select * from users"
    rows = await database.fetch_all(query=query)

    for row in rows:
        if row['username'] == user.username or row['password'] == user.password:
            raise HTTPException(
                status_code=406, detail="This username or password exists, please choose a different one")

    query = "insert into users(username,password,private_images,public_images) values ('{username}','{password}',{private_images},{public_images})".format(username=user.username, password=user.password,
                                                                                                                                                           private_images=0, public_images=0)
    last_record_id = await database.execute(query)
    return {**user.dict()}
