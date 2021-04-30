from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    ForeignKey
)
from .db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum


class PermissionsEnum(enum.Enum):
    private = 'private'
    public = 'public'


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String)
    password = Column("password", String)
    private_images = Column("private_images", Integer)
    public_images = Column("public_images", Integer)
    date_created = Column("date_created", DateTime(
        timezone=True), server_default=func.now())
    date_updated = Column("date_updated", DateTime(
        timezone=True), server_default=func.now())

    image = relationship("Image", back_populates="images")


class Image(Base):
    __tablename__ = "images"

    id = Column("id", Integer, primary_key=True, index=True)
    permissions = Column("permissions", String)
    text = Column("text", String)
    characteristics = Column("characteristics", String)
    date_created = Column("date_created", DateTime(
        timezone=True), server_default=func.now())
    user_id = Column("user_id", Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="users")
