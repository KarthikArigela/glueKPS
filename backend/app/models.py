from datetime import datetime
from sqlmodel import SQLModel, Field

class HealthLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_name: str
    status: str
    checked_at: datetime = Field(default_factory=datetime.utcnow)