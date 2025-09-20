from typing import Generator
from sqlmodel import Session
from app.core.config import engine


SessionLocal = Session(engine)

def get_session() -> Generator :
    """
    Function to inject db session in a endpoint.
    It's closed post use.
    """

    db_session = SessionLocal

    try:
        yield db_session
    
    finally:
        db_session.close()