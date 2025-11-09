from sqlmodel import SQLModel
from typing import Optional

from app.models.users import UserTypeEnum
from app.models.org_user import StatusEnum

class OrgUserCreate(SQLModel):
    org_id : str
    user_id : str
    type : UserTypeEnum
    role : Optional[str] = None
    
class OrgUserUpdate(SQLModel):
    status : StatusEnum
    role : Optional[str]