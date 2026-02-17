from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import engine,get_db
from .routers import posts,user,auth,votes
from .config import settings
from .database import engine
from sqlalchemy.orm import Session
from sqlalchemy import text,inspect
import sqlalchemy
from alembic.config import Config
from alembic import command
import os


with engine.connect() as conn:
    # This force-deletes the tables so we can start fresh
    conn.execute(text("DROP TABLE IF EXISTS posts, users, votes, alembic_version CASCADE;"))
    conn.commit()




app = FastAPI()
origins = ["https://www.google.com","https://www.youtube.com"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials = True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/verify-db")
def verify_db():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    
    # Check the default 'public' schema
    public_tables = inspector.get_table_names(schema="public")
    
    # Check if they were created under a different schema name
    all_schemas = inspector.get_schema_names()
    
    return {
        "database_host": str(engine.url).split('@')[-1],
        "public_schema_tables": public_tables,
        "available_schemas": all_schemas,
        "note": "If public_schema_tables is empty, check the other schemas listed."
    }


@app.get("/force-migrate")
def force_migrate():
    try:
        # This points to the alembic.ini in your root folder
        alembic_cfg = Config("alembic.ini")
        # This forces alembic to use the LIVE engine URL
        alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL").replace("postgres://", "postgresql://"))
        command.upgrade(alembic_cfg, "head")
        return {"status": "success", "message": "Migrations forced successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}





