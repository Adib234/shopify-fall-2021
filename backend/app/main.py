from fastapi import FastAPI

from . import models
from .controllers import (add, create_user, delete, my_images, my_info, root,
                          search)
from .db import database, engine

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
app.include_router(add.router, prefix='/add')
app.include_router(delete.router, prefix='/delete')
app.include_router(my_images.router, prefix='/my_images')
app.include_router(search.router, prefix="/search")
