"""Router for feed-related events."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from events.feed.service import FeedService
from events.feed import schemas
from persistence.dependencies import get_db

router = APIRouter()


@router.post("/bottle", response_model=schemas.FeedBottleEvent)
def create_bottle_feed_event(
    event: schemas.FeedBottleEvent, db: Session = Depends(get_db)
):
    """Create a new bottle feed event."""
    service = FeedService(db=db)
    return service.create_bottle_feed_event(event=event)


@router.get("/bottle/{event_id}", response_model=schemas.FeedBottleEvent)
def get_bottle_feed_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve a bottle feed event by its ID."""
    service = FeedService(db=db)
    return service.get_bottle_feed_event(event_id=event_id)


@router.put("/bottle/{event_id}", response_model=schemas.FeedBottleEvent)
def update_bottle_feed_event(
    event_id: str, event: schemas.FeedBottleEvent, db: Session = Depends(get_db)
):
    """Update an existing bottle feed event."""
    service = FeedService(db=db)
    return service.update_bottle_feed_event(event_id=event_id, event=event)
