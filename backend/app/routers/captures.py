import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Capture
from app.schemas import CaptureCreate, CaptureRead

router = APIRouter()

@router.post(
    "/",
    response_model=CaptureRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new raw capture"
)
async def create_capture(
    payload: CaptureCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new raw text capture entry in DB."""
    
    db_capture = Capture(
        raw_text=payload.raw_text,
        kind=payload.kind,
        state="pending_clarification"
    )

    session.add(db_capture)
    await session.commit()
    await session.refresh(db_capture)
    return db_capture

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
    """Retrieve a single capture by its UUID."""

    capture = await session.get(Capture, capture_id)
    
    if not capture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capture with ID '{capture_id}' not found."
        )
    
    return capture
