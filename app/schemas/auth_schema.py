from app.models.user import UserTypeEnum
from pydantic import BaseModel

class AuthSchema(BaseModel):
    email : str 
    password : str
    type : UserTypeEnum


class Token(BaseModel):
    access_token : str
    token_type : str