from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from typing import ClassVar
from user import UserTypeEnum
from enum import Enum
import uuid


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"

class StatusEnum(str, Enum):
    ACTIVE = 'ACTIVE'
    FINISHED = "FINISHED"

class OrgUser(SQLModel, table=True):
    __tablename__ : ClassVar[str] = "org_user" #type:ignore

    org_id : uuid.UUID  = Field(foreign_key="organization.id", primary_key=True)
    user_id : uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    type : UserTypeEnum = Field(primary_key=True)
    role : RoleEnum = Field(default=None)
    status : StatusEnum = Field(default=StatusEnum.ACTIVE)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        sa_column_kwargs={"onupdate": None} 
    )
    finished_at : datetime = Field(default=None)