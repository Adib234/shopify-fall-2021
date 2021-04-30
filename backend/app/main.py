from fastapi import FastAPI

from .controllers import root, create_user, my_info, add
from .db import engine, database
from . import models

models.Base.metadata.create_all(bind=engine)

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
app.include_router(add.router)
