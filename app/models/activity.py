import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class ActitivityStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Activity(SQLModel, table=True):
    __tablename__ = "activity"
    __table_args__ = {"schema" : "core"}

    id : uuid.UUID  = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id : uuid.UUID  = Field(foreign_key="core.organization.id")
    user_id : uuid.UUID  = Field(foreign_key="core.users.id")
    name : str = Field()
    description : str = Field()
    status : ActitivityStatus = Field(default=ActitivityStatus.PENDING)
    start_time : datetime = Field()
    end_time : datetime = Field()
    approved_by : uuid.UUID  = Field(foreign_key="core.users.id", default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        sa_column_kwargs={"onupdate": None} 
    )