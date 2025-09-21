from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate

def get_user_by_id(db : Session, user_id : UUID) -> Optional[User]:
    """
    Returns a User by an id
    """
    return db.exec(select(User).where(User.id == user_id)).first()

def get_user_by_email(db : Session, user_email : str) -> Optional[User]:
    """
    Returns a User by an email
    """
    return db.exec(select(User).where(User.email == user_email)).first()

def get_all_users(db : Session) -> List[User]:
    """
    Returns all Users stored in db
    """
    result =  db.exec(select(User)).all()

    return list(result)

def create_user(db : Session, user_in : UserCreate) -> User:
    """
    Creates a new User
    """
    user = User.model_validate(user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db : Session, user : User, user_in : UserUpdate) -> User:
    """
    Updates a User
    """
    for key, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db : Session, user : User):
    """
    Deletes a User
    """
    db.delete(user)
    db.commit()