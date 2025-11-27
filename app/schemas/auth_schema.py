from app.models.users import UserTypeEnum
from pydantic import BaseModel
from uuid import UUID

class AuthSchema(BaseModel):
    email : str 
    password : str
    type : UserTypeEnum


class UserResponseSchema(BaseModel):
    id : UUID
    name : str
    email : str
    type : UserTypeEnum

class LoginResponseSchema(BaseModel):
    user : UserResponseSchema
    access_token : str
    token_type : str = "Bearer"
    org_id : UUID

class Token(BaseModel):
    access_token : str
    token_type : str

class Current_User(BaseModel):
    id : str
    type : UserTypeEnum
    org_id : str
    email : str
    name : str
    org_id : str