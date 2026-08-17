import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CaptureCreate(BaseModel):
    raw_text: str = Field(
        ...,
        min_length=1,
        description="The raw text ramble or thought input by the user."
    )
    kind: str = Field(
        default="text",
        description="Source type of capture (e.g., text, voice)."
    )

class CaptureRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None = None
    raw_text: str
    kind: str
    state: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)