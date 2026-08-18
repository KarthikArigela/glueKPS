import pytest
from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_adapter import OpenAIResponsesAdapter
from app.services.ai_telemetry import record_ai_operation
from app.models import AIOperation

class TestSummary(BaseModel):
    summary: str
    category: str

@pytest.mark.anyio
async def test_ai_telemetry_recording(async_session: AsyncSession):
    """Test recording an AI operation into the ai_operations database table."""

    mock_prompt = "Explain quantum computing in 1 sentence."
    mock_response = '{"summary": "Quantum computing uses qubits for superdense computation.", "category": "physics"}'
    mock_latency = 245.5

    op_record = await record_ai_operation(
        session=async_session,
        provider="openai",
        model="gpt-5.6-luna",
        prompt=mock_prompt,
        response=mock_response,
        latency_ms=mock_latency,
        cost_estimate_usd=0.0001
    )

    assert op_record.id is not None
    assert op_record.provider == "openai"
    assert op_record.latency_ms == 245.5

    statement = select(AIOperation).where(AIOperation.id == op_record.id)
    result = await async_session.execute(statement)
    db_op = result.scalar_one()
    assert db_op.prompt == mock_prompt