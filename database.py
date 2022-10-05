import os

import sqlalchemy
import sqlalchemy.ext.declarative as declarative
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DB_URL", "postgresql://root:root@localhost:5432/delivery-db")

engine = sqlalchemy.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseORM = declarative.declarative_base()
