from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os


# This ensures the app uses the URL provided by Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for Render's 'postgres://' vs 'postgresql://' issue
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base() # Used to define the Schema for the database


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_dATABASE_URL = "postgresql://postgres:0722jkdkeLL@localhost/fastapi"

# engine = create_engine(SQLALCHEMY_dATABASE_URL)

# sessionlocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

# def get_db():
#     db = sessionlocal()

#     try:
#         yield db
#     finally:
#         db.close()


