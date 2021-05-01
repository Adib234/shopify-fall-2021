import os

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()
DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)

# databases query builder
database = Database(DATABASE_URL)
