from sqlalchemy.orm import Session
from structlog import get_logger
from events.feed.model_schema_translation import FeedModelSchemaTranslation
from events.feed import schemas, models
from fastapi import HTTPException, status


class FeedPersistence:
    def __init__(self, db: Session):
        self._log = get_logger()
        self._db = db
        self._translation = FeedModelSchemaTranslation()

    def insert_bottle_feed_event(
        self, event: schemas.FeedBottleEvent
    ) -> schemas.FeedBottleEvent:
        """Insert a new bottle feed event into the database."""
        self._log.debug("Inserting bottle feed event", evt=event)

        model = self._translation.bottle_feed_schema_to_model(schema=event)

        try:
            self._db.add(model.event)
            self._db.add(model)

            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to insert bottle feed event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Bottle feed event inserted successfully", model=model)

        return self._translation.bottle_feed_model_to_schema(model=model)

    def get_bottle_feed_event(self, event_id: str) -> schemas.FeedBottleEvent:
        """Retrieve a bottle feed event by its ID."""
        self._log.debug("Retrieving bottle feed event", event_id=event_id)

        model = (
            self._db.query(models.FeedBottleEvent)
            .filter(models.FeedBottleEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Bottle feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Bottle feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self._log.debug("Bottle feed event retrieved successfully", model=model)

        return self._translation.bottle_feed_model_to_schema(model=model)

    def update_bottle_feed_event(
        self, event_id: str, event: schemas.FeedBottleEvent
    ) -> schemas.FeedBottleEvent:
        """Update an existing bottle feed event."""
        self._log.debug("Updating bottle feed event", event_id=event_id, evt=event)

        model = (
            self._db.query(models.FeedBottleEvent)
            .filter(models.FeedBottleEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Bottle feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Bottle feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        updated_model = self._translation.bottle_feed_schema_to_model(schema=event)

        for key, value in updated_model.__dict__.items():
            if key != "id":  # Avoid changing the ID
                setattr(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to update bottle feed event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Bottle feed event updated successfully", model=model)

        return self._translation.bottle_feed_model_to_schema(model=model)

    def delete_bottle_feed_event(self, event_id: str) -> None:
        """Delete a bottle feed event by its ID."""
        self._log.debug("Deleting bottle feed event", event_id=event_id)

        model = (
            self._db.query(models.FeedBottleEvent)
            .filter(models.FeedBottleEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Bottle feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Bottle feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self._log.error("Failed to delete bottle feed event", error=repr(e))
            self._db.rollback()
            raise
