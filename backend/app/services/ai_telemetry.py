import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AIOperation

async def record_ai_operation(
    session: AsyncSession,
    provider: str,
    model: str,
    prompt: str,
    response: str,
    latency_ms: float,
    user_id: uuid.UUID | None = None,
    capture_id: uuid.UUID | None = None,
    cost_estimate_usd: float = 0.0,
    confidence_score: float | None = None,
) -> AIOperation:
    """Logs an AI execution operation into the ai_operations database table."""

    operation = AIOperation(
        user_id=user_id,
        capture_id=capture_id,
        provider=provider,
        model=model,
        prompt=prompt,
        response=response,
        latency_ms=latency_ms,
        cost_estimate_usd=cost_estimate_usd,
        confidence_score=confidence_score,
    )
    session.add(operation)
    await session.commit()
    await session.refresh(operation)
    return operation