from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime


from app.models.users import UserTypeEnum

class UserCreate(SQLModel):
    name : str
    surname : Optional[str] = None
    email : str
    password : str
    type : UserTypeEnum
    company_name : Optional[str] = None
    cnpj : Optional[str] = None
    code : Optional[str] = None
    supervisor_max_amount : Optional[int] = 1

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

class UserWithoutPassword(SQLModel):
    id: UUID
    name: str
    surname: Optional[str] = None
    email: str
    type: UserTypeEnum
