import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class UserTypeEnum(str, Enum):
    STUDENT = "STUDENT"
    SUPERVISOR = "SUPERVISOR"


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"schema" : "core"}

    id : uuid.UUID  = Field(default_factory=uuid.uuid4, primary_key=True)
    name : str = Field()
    surname : str | None = Field(default=None)
    email : str = Field(unique=True)
    password : str = Field()
    type : UserTypeEnum = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        sa_column_kwargs={"onupdate": None} 
    )