from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime


from app.models.user import UserTypeEnum

class UserCreate(SQLModel):
    name : str
    surname : Optional[str] = None
    email : str
    password : str
    type : UserTypeEnum

class UserUpdate(SQLModel):
    name : Optional[str] = None
    surname : Optional[str] = None
    email : Optional[str] = None 
    password : Optional[str] = None 
    type : Optional[UserTypeEnum] = None

class UserRead(SQLModel):
    id: UUID
    name: str
    surname: Optional[str] = None
    email: str
    type: UserTypeEnum
    created_at: datetime
