import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Capture
from app.schemas import CaptureCreate, CaptureRead, ClarifyAnswerCreate, ClarificationResponse
from app.services.clarification_engine import ClarificationEngine

router = APIRouter()

@router.post(
    "/",
    response_model=ClarificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new capture and initialize clarification"
)
async def create_capture(
    payload: CaptureCreate,
    session: AsyncSession = Depends(get_session)
):
    """Creates a new raw capture entry in DB AND automatically initializes Turn 1 of Clarification!"""
    
    db_capture = Capture(raw_text=payload.raw_text, kind=payload.kind)

    session.add(db_capture)
    await session.commit()
    await session.refresh(db_capture)

    engine = ClarificationEngine()
    return await engine.process_clarification(session, db_capture)

@router.get(
    "/",
    response_model=list[CaptureRead],
    status_code=status.HTTP_200_OK,
    summary="List all captures"
)
async def list_captures(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve list of all captures, ordered by newest first."""

    statement = (
        select(Capture)
        .order_by(Capture.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    result = await session.execute(statement)
    captures = result.scalars().all()
    return captures

@router.get(
    "/{capture_id}",
    response_model=CaptureRead,
    status_code=status.HTTP_200_OK,
    summary="Get a single capture by ID"
)
async def get_capture(
    capture_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    """Fetch a single capture by ID."""

    capture = await session.get(Capture, capture_id)
    
    if not capture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capture with ID '{capture_id}' not found."
        )
    
    return capture

@router.post(
    "/{capture_id}/clarify", 
    response_model=ClarificationResponse,
    summary="Continue Clarification"
)
async def clarify_capture(
    capture_id: uuid.UUID,
    payload: ClarifyAnswerCreate | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Appends user answer (or resumes active thread) and processes the next clarification turn."""
    statement = select(Capture).where(Capture.id == capture_id)
    result = await session.execute(statement)
    capture = result.scalar_one_or_none()

    if not capture:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    engine = ClarificationEngine()
    user_answer = payload.answer if payload else None
    
    response = await engine.process_clarification(
        session=session,
        capture=capture,
        user_answer=user_answer
    )
    
    return response
