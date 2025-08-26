"""Router for diaper-related events."""

from fastapi import APIRouter, Depends
from typing import Sequence
from sqlalchemy.orm import Session
from events.diaper.service import DiaperService
from events.diaper import schemas
from persistence.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.DiaperEvent)
def create_diaper_event(event: schemas.DiaperEvent, db: Session = Depends(get_db)):
    """Create a new diaper event."""
    service = DiaperService(db=db)
    return service.create_diaper_event(event=event)


@router.get("/{event_id}", response_model=schemas.DiaperEvent)
def get_diaper_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve a diaper event by its ID."""
    service = DiaperService(db=db)
    return service.get_diaper_event(event_id=event_id)


@router.get("/", response_model=Sequence[schemas.DiaperEvent])
def list_diaper_events(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
):
    """List diaper events with pagination."""
    service = DiaperService(db=db)
    return service.list_diaper_events(limit=limit, offset=offset)


@router.put("/{event_id}", response_model=schemas.DiaperEvent)
def update_diaper_event(
    event_id: str, event: schemas.DiaperEvent, db: Session = Depends(get_db)
):
    """Update an existing diaper event."""
    service = DiaperService(db=db)
    return service.update_diaper_event(event_id=event_id, event=event)


@router.delete("/{event_id}")
def delete_diaper_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a diaper event by its ID."""
    service = DiaperService(db=db)
    service.delete_diaper_event(event_id=event_id)
    return {"message": "Diaper event deleted successfully."}
