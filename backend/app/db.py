import os
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from databases import Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)

# databases query builder
database = Database(DATABASE_URL)
