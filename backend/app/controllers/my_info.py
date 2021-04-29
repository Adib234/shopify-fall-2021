from ..db import database
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter()
security = HTTPBasic()


async def validate(username: str, password: str) -> bool:
    """
    Checks to see if the user has registered before
    """
    validated = False
    query = "select * from users"
    rows = await database.fetch_all(query=query)
    for row in rows:
        if row['username'] == username and row['password'] == password:
            validated = True
            break
    return validated


@router.get("/my_info/")
async def my_info(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Gets the information of the current user:
    :param credentials: User input.
        - **username**: 
        - **password**: 
    Returns an dictionary with the following information: Username, Password, Number of public images, Number 
    of private images
    """
    value = await validate(credentials.username, credentials.password)
    print(value)
    if not value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    query = "select * from users where users.username='{user}' and users.password='{password}'".format(
        user=credentials.username, password=credentials.password)
    result = await database.fetch_all(query=query)
    return {"Username": result[0]['username'], "Password": result[0]['password'], "Private images": result[0]['private_images'], "Public images": result[0]['public_images']}
