from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import engine,get_db
from .routers import posts,user,auth,votes
from .config import settings
from .database import engine
from sqlalchemy.orm import Session
from sqlalchemy import text,inspect



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
def verify_db(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {
            "connection": "Live",
            "database_host": str(engine.url).split('@')[-1], # Shows you the server name
            "existing_tables": tables
        }






