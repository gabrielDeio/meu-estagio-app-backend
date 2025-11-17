from app.models.users import UserTypeEnum
from pydantic import BaseModel

class AuthSchema(BaseModel):
    email : str 
    password : str
    type : UserTypeEnum


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