import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, TEXT

class HealthLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_name: str
    status: str
    checked_at: datetime = Field(default_factory=datetime.utcnow)

class Capture(SQLModel, table=True):
    __tablename__ = "captures"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID | None = Field(default=None, index=True, nullable=True)
    raw_text: str = Field(sa_column=Column(TEXT, nullable=False))
    kind: str = Field(default="text", nullable=False)
    state: str = Field(default="pending_clarification", nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class AIOperation(SQLModel, table=True):
    __tablename__ = "ai_operations"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID | None = Field(default=None, index=True, nullable=True)
    capture_id: uuid.UUID | None = Field(default=None, index=True, nullable=True)
    
    provider: str = Field(default="openrouter", nullable=False)
    model: str = Field(nullable=False)
    prompt: str = Field(sa_column=Column(TEXT, nullable=False))
    response: str = Field(sa_column=Column(TEXT, nullable=False))
    latency_ms: float = Field(nullable=False)
    cost_estimate_usd: float = Field(default=0.0, nullable=False)
    confidence_score: float | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)