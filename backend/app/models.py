from sqlalchemy import (Column, DateTime, ForeignKey, Integer, LargeBinary,
                        String, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


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
    s3_name = Column("s3_name", String)
    original_name = Column("org_name", String)
    permissions = Column("permissions", String)
    text = Column("text", String)
    characteristics = Column("characteristics", String)
    date_created = Column("date_created", DateTime(
        timezone=True), server_default=func.now())
    user_id = Column("user_id", Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="users")
