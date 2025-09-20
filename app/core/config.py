import os 
from sqlmodel import create_engine
from sqlalchemy.engine import Engine

DATABASE_URL : str | None = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("Database config string env not configured")

engine : Engine = create_engine(DATABASE_URL)