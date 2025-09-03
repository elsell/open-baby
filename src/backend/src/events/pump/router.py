"""Router for pump-related events."""

from fastapi import APIRouter, Depends
from typing import Sequence
from sqlalchemy.orm import Session
from events.pump.service import PumpService
from events.pump import schemas
from persistence.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.PumpEvent)
def create_pump_event(event: schemas.PumpEvent, db: Session = Depends(get_db)):
    """Create a new pump event."""
    service = PumpService(db=db)
    return service.create_pump_event(event=event)


@router.get("/{event_id}", response_model=schemas.PumpEvent)
def get_pump_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve a pump event by its ID."""
    service = PumpService(db=db)
    return service.get_pump_event(event_id=event_id)


@router.get("/", response_model=Sequence[schemas.PumpEvent])
def list_pump_events(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    """List pump events with pagination."""
    service = PumpService(db=db)
    return service.list_pump_events(limit=limit, offset=offset)


@router.put("/{event_id}", response_model=schemas.PumpEvent)
def update_pump_event(
    event_id: str, event: schemas.PumpEvent, db: Session = Depends(get_db)
):
    """Update an existing pump event."""
    service = PumpService(db=db)
    return service.update_pump_event(event_id=event_id, event=event)


@router.delete("/{event_id}")
def delete_pump_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a pump event by its ID."""
    service = PumpService(db=db)
    service.delete_pump_event(event_id=event_id)
    return {"message": "Pump event deleted successfully."}
