from typing import Optional
from sqlmodel import SQLModel


from app.models.user import UserTypeEnum

class UserCreate(SQLModel):
    name : str
    surname : Optional[str]
    email : str
    password : str
    type : UserTypeEnum

class UserUpdate(SQLModel):
    name : Optional[str]
    surname : Optional[str]
    email : Optional[str]
    password : Optional[str]
    type : Optional[UserTypeEnum]


