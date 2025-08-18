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
