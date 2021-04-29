from ..schemas import user
from ..db import database
from ..models.users import users
from fastapi import HTTPException, APIRouter

router = APIRouter()


@router.post("/create_user/", response_model=user.User)
async def create_user(user: user.User):
    """
    Create a user with all the information:
    :param user: User input.
        - **username**: username to access their private repositories (required)
        - **password**: password to access their private repositories (required)
    Returns the values that they entered (username, password)
    """
    duplicate = False
    query = "select * from users"
    rows = await database.fetch_all(query=query)
    for row in rows:
        if row['username'] == user.username:
            raise HTTPException(
                status_code=404, detail="This username exists, please choose a different one")

        elif row['password'] == user.password:
            raise HTTPException(
                status_code=404, detail="This password exists, please choose a different one")

    query = users.insert().values(username=user.username, password=user.password,
                                  private_images=0, public_images=0)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
