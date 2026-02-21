from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os



# This ensures the app uses the URL provided by Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEM_DATABASE_INTERNAL_URL = (
    "postgresql://" + 
    f"{settings.database_username}:{settings.database_password}@" + 
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
print(f"--- DEBUG CHECK ---")
print(f"DATABASE_URL exists: {os.getenv('DATABASE_URL') is not None}")
print(f"Final URL being used: {SQLALCHEMY_DATABASE_URL}")

if SQLALCHEMY_DATABASE_URL is not None:

# Fix for Render's 'postgres://' vS 'postgresql://' issue
    if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_URL = SQLALCHEMY_DATABASE_URL

else:
    SQLALCHEMY_URL = SQLALCHEM_DATABASE_INTERNAL_URL


engine = create_engine(SQLALCHEMY_URL) # the engine for the sqlalchemy is always open for commiting changes in the data while that for the alembic opens only when it is running migrations on making changes in the database by placing the tables or columns that are on the declarative base
print(f"DEBUG: FastAPI is connecting to: {engine.url}")
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


