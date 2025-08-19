from sqlalchemy.orm import Session
from structlog import get_logger
from events.feed.model_schema_translation import FeedModelSchemaTranslation
from events.feed import schemas, models
from fastapi import HTTPException, status
from sqlalchemy.orm.attributes import set_attribute


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

        try:
            model = (
                self._db.query(models.FeedBottleEvent)
                .filter(models.FeedBottleEvent.id == event_id)
                .first()
            )
        except LookupError as e:
            self._log.error("Invalid event type", error=repr(e))
            raise HTTPException(
                detail=f"Invalid event type for ID {event_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            self._log.error("Bottle feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Bottle feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        for key, value in event.model_dump().items():
            if key != "id":  # Avoid changing the ID
                set_attribute(model, key, value)

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

    def insert_breast_feed_event(
        self, event: schemas.FeedBreastEvent
    ) -> schemas.FeedBreastEvent:
        """Insert a new breast feed event into the database."""
        self._log.debug("Inserting breast feed event", evt=event)

        model = self._translation.breast_feed_schema_to_model(schema=event)

        try:
            self._db.add(model)
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to insert breast feed event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Breast feed event inserted successfully", model=model)

        return self._translation.breast_feed_model_to_schema(model=model)

    def get_breast_feed_event(self, event_id: str) -> schemas.FeedBreastEvent:
        """Retrieve a breast feed event by its ID."""
        self._log.debug("Retrieving breast feed event", event_id=event_id)

        model = (
            self._db.query(models.FeedBreastEvent)
            .filter(models.FeedBreastEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Breast feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Breast feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self._log.debug("Breast feed event retrieved successfully", model=model)

        return self._translation.breast_feed_model_to_schema(model=model)

    def update_breast_feed_event(
        self, event_id: str, event: schemas.FeedBreastEvent
    ) -> schemas.FeedBreastEvent:
        """Update an existing breast feed event."""
        self._log.debug("Updating breast feed event", event_id=event_id, evt=event)

        try:
            model = (
                self._db.query(models.FeedBreastEvent)
                .filter(models.FeedBreastEvent.id == event_id)
                .first()
            )
        except LookupError as e:
            self._log.error("Invalid event type", error=repr(e))
            raise HTTPException(
                detail=f"Invalid event type for ID {event_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            self._log.error("Breast feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Breast feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        for key, value in event.model_dump().items():
            if key != "id":  # Avoid changing the ID
                set_attribute(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to update breast feed event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Breast feed event updated successfully", model=model)

        return self._translation.breast_feed_model_to_schema(model=model)

    def delete_breast_feed_event(self, event_id: str) -> None:
        """Delete a breast feed event by its ID."""
        self._log.debug("Deleting breast feed event", event_id=event_id)

        model = (
            self._db.query(models.FeedBreastEvent)
            .filter(models.FeedBreastEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Breast feed event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Breast feed event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self._log.error("Failed to delete breast feed event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Breast feed event deleted successfully", event_id=event_id)

        return None
