from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime

from app.models.activity import ActitivityStatus


class ActivityCreate(SQLModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    org_id : str
    user_id : str


class ActivityUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status : Optional[ActitivityStatus] = None
    approved_by : Optional[UUID] = None
