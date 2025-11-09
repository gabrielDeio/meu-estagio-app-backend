from typing import Optional
from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime

class OrganizationCreate(SQLModel):
    name : str
    supervisor_max_amount : Optional[int] = 1
    cnpj : str

class OrganizationUpdate(SQLModel):
    name : Optional[str] = None
    supervisor_max_amount : Optional[int] = None


class OrganizationRead(SQLModel):
    id : UUID
    name : str
    supervisor_max_amount : int
    cnpj : str
    created_at: datetime