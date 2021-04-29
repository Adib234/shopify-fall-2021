from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
)
from ..db import metadata
from sqlalchemy.sql import func

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("password", String),
    Column("private_images", Integer),
    Column("public_images", Integer),
    Column("date_created", DateTime(timezone=True), server_default=func.now())
)
