from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from app.models.users import Users
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.hash import get_password_hash
from app.models.users import UserTypeEnum

def get_user_by_id(db : Session, user_id : UUID, user_type : UserTypeEnum) -> Optional[Users]:
    """
    Returns a User by an id
    """
    return db.exec(select(Users).where(Users.id == user_id)).first()

def get_user_by_email(db : Session, user_email : str, user_type : UserTypeEnum) -> Optional[Users]:
    """
    Returns a User by an email
    """
    return db.exec(select(Users).where(Users.email == user_email, Users.type == user_type)).first()

def get_all_users(db : Session) -> List[Users]:
    """
    Returns all Users stored in db
    """
    result =  db.exec(select(Users)).all()

    return list(result)

def create_user(db : Session, user_in : UserCreate) -> Users:
    """
    Creates a new User
    """
    user_data = user_in.model_dump()
    user_data["password"] = get_password_hash(user_data["password"])

    user = Users(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db : Session, user : Users, user_in : UserUpdate) -> Users:
    """
    Updates a User
    """
    for key, value in user_in.model_dump(exclude_unset=True).items():
        if(key == "password"):
            value = get_password_hash(value)

        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db : Session, user : Users):
    """
    Deletes a User
    """
    db.delete(user)
    db.commit()