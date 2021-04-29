from .db import database
from fastapi import HTTPException, status


async def authenticate(api_key):
    query = "select *  from ( select concat(username,password) as api_key from users) users where users.api_key='{api_key}'".format(
            api_key=api_key)
    authenticate = await database.fetch_all(query=query)
    if not len(authenticate) == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect API key",
        )
