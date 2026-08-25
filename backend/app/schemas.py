import uuid
from datetime import datetime
from typing import Literal
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
    outcome: str | None = None
    kind: str
    state: str
    clarification_history: list[dict]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LLMClarificationOutput(BaseModel):
    """Structured Pydantic schema enforced on LLM output via OpenAI Responses API."""
    classification: Literal["project", "task", "not_actionable"] = Field(
        ..., 
        description="Assessed category of the intention based on context."
    )
    status: Literal["question", "ready_for_proposal", "terminal"] = Field(
        ..., 
        description="'question' if more info is needed, 'ready_for_proposal' if enough details gathered, 'terminal' if not actionable."
    )
    outcome: str | None = Field(
        default=None,
        description="The synthesized, clear 1-sentence outcome of what the user wants to accomplish."
    )
    question: str | None = Field(
        default=None, 
        description="The SINGLE focused clarifying question to ask the user. Null if ready_for_proposal or terminal."
    )
    reasoning: str = Field(
        ..., 
        description="Brief 1-sentence reasoning behind the question or classification."
    )
    summary_so_far: str | None = Field(
        default=None,
        description="Concise synthesis of what is known so far about the project/task."
    )

class ClarifyAnswerCreate(BaseModel):
    """Request payload when user submits an answer to a clarification question."""
    answer: str = Field(
        ..., 
        min_length=1, 
        description="User's response to the clarifying question."
    )

class ClarificationResponse(BaseModel):
    """API response payload returned to the frontend."""
    capture_id: uuid.UUID
    state: str
    classification: str
    status: str
    question: str | None
    reasoning: str
    summary_so_far: str | None
    messages: list[dict]