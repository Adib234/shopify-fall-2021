from .db import database

# Get info of a user after getting a valid api key


async def request_user(info, api_key):
    query = "select *  from ( select concat(username,password) as {info} from users) users where users.api_key='{api_key}'".format(
        info=info, api_key=api_key)
    result = await database.fetch_all(query=query)
    return result
