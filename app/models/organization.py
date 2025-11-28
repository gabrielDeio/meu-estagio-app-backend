import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Organization(SQLModel, table=True):
    __tablename__ = "organization"
    __table_args__ = {"schema" : "core"}
    
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name : str = Field()
    supervisor_max_amount : int = Field()
    cnpj : str = Field()
    code : str = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        sa_column_kwargs={"onupdate": None} 
    )