import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import func
from databases import Database


DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# databases query builder
database = Database(DATABASE_URL)
