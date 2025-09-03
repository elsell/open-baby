"""Router for events."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import structlog
from events.service import EventService
from events import schemas
from persistence.dependencies import get_db
import datetime
from events.feed.router import router as feed_router
from events.diaper.router import router as diaper_router
from events.pump.router import router as pump_router

router = APIRouter()

log = structlog.get_logger()

router.include_router(feed_router, prefix="/feed", tags=["feed"])
router.include_router(diaper_router, prefix="/diaper", tags=["diaper"])
router.include_router(pump_router, prefix="/pump", tags=["pump"])


@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.Event, db: Session = Depends(get_db)):
    """Create a new event."""
    service = EventService(db=db)
    return service.create_event(event=event)


@router.get("/{event_id}", response_model=schemas.Event)
def get_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve a event by its ID."""
    service = EventService(db=db)
    return service.get_event(event_id=event_id)


@router.get("/", response_model=schemas.EventListResponse)
def list_events(
    limit: int = 100,
    offset: int = 0,
    start_time: datetime.datetime = Query(
        None, description="ISO 8601 format e.g. 2023-01-01T12:00:00Z"
    ),
    end_time: datetime.datetime = Query(
        None, description="ISO 8601 format e.g. 2023-01-01T12:00:00Z"
    ),
    db: Session = Depends(get_db),
):
    """List events with pagination and time window filtering."""
    service = EventService(db=db)
    return service.list_events(
        limit=limit, offset=offset, start_time=start_time, end_time=end_time
    )


@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: str, event: schemas.Event, db: Session = Depends(get_db)):
    """Update an existing event."""
    service = EventService(db=db)
    return service.update_event(event_id=event_id, event=event)


@router.delete("/{event_id}")
def delete_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a event by its ID."""
    service = EventService(db=db)
    service.delete_event(event_id=event_id)
    return {"message": "Event deleted successfully."}
