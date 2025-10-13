import os 
from sqlmodel import create_engine, SQLModel
from sqlalchemy.engine import Engine
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL : str | None = os.getenv("DATABASE_URL")
SECRET_KEY : str | None = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES : str | None = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ENCODE_ALGORITHM : str | None = os.getenv("ENCODE_ALGORITHM")

if DATABASE_URL is None:
    raise ValueError("Database config string env not configured")


engine : Engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)