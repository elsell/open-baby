"""Router for feed-related events."""

from fastapi import APIRouter, Depends
from typing import Sequence
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


@router.get("/bottle", response_model=Sequence[schemas.FeedBottleEvent])
def list_bottle_feed_events(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
):
    """List bottle feed events with pagination."""
    service = FeedService(db=db)
    return service.list_bottle_feed_events(limit=limit, offset=offset)


@router.put("/bottle/{event_id}", response_model=schemas.FeedBottleEvent)
def update_bottle_feed_event(
    event_id: str, event: schemas.FeedBottleEvent, db: Session = Depends(get_db)
):
    """Update an existing bottle feed event."""
    service = FeedService(db=db)
    return service.update_bottle_feed_event(event_id=event_id, event=event)


@router.delete("/bottle/{event_id}")
def delete_bottle_feed_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a bottle feed event by its ID."""
    service = FeedService(db=db)
    service.delete_bottle_feed_event(event_id=event_id)
    return {"message": "Bottle feed event deleted successfully."}


@router.post("/breast", response_model=schemas.FeedBreastEvent)
def create_breast_feed_event(
    event: schemas.FeedBreastEvent, db: Session = Depends(get_db)
):
    """Create a new breast feed event."""
    service = FeedService(db=db)
    return service.create_breast_feed_event(event=event)


@router.get("/breast/{event_id}", response_model=schemas.FeedBreastEvent)
def get_breast_feed_event(event_id: str, db: Session = Depends(get_db)):
    """Retrieve a breast feed event by its ID."""
    service = FeedService(db=db)
    return service.get_breast_feed_event(event_id=event_id)


@router.get("/breast", response_model=Sequence[schemas.FeedBreastEvent])
def list_breast_feed_events(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
):
    """List breast feed events with pagination."""
    service = FeedService(db=db)
    return service.list_breast_feed_events(limit=limit, offset=offset)


@router.put("/breast/{event_id}", response_model=schemas.FeedBreastEvent)
def update_breast_feed_event(
    event_id: str, event: schemas.FeedBreastEvent, db: Session = Depends(get_db)
):
    """Update an existing breast feed event."""
    service = FeedService(db=db)
    return service.update_breast_feed_event(event_id=event_id, event=event)


@router.delete("/breast/{event_id}")
def delete_breast_feed_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a breast feed event by its ID."""
    service = FeedService(db=db)
    service.delete_breast_feed_event(event_id=event_id)
    return {"message": "Breast feed event deleted successfully."}
