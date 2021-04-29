from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    ForeignKeyConstraint,
    Enum
)
from sqlalchemy.sql import func
from ..db import metadata
from .users import users


class PermissionsEnum(Enum):
    private = 'private'
    public = 'public'


images = Table("images", metadata,
               Column("id", Integer, primary_key=True),
               Column("permissions", Enum("private", "public",
                                          name="PermissionsEnum"), default="public"),
               Column("text", String),
               Column("characteristics", String),
               Column("date_created", DateTime(
                   timezone=True), server_default=func.now()),
               ForeignKeyConstraint(['id'], ['users.id']))
