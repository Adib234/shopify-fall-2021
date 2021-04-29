from fastapi import FastAPI

from .controllers import root, create_user, my_info
from .db import engine, database, metadata

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(root.router)
app.include_router(create_user.router)
app.include_router(my_info.router)
