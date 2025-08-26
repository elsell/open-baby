from typing import Sequence
from sqlalchemy.orm import Session
from structlog import get_logger
from events.diaper.model_schema_translation import DiaperModelSchemaTranslation
from events.diaper import schemas, models
from fastapi import HTTPException, status
from sqlalchemy.orm.attributes import set_attribute


class DiaperPersistence:
    def __init__(self, db: Session):
        self._log = get_logger()
        self._db = db
        self._translation = DiaperModelSchemaTranslation()

    def insert_diaper_event(self, event: schemas.DiaperEvent) -> schemas.DiaperEvent:
        """Insert a new diaper event into the database."""
        self._log.debug("Inserting diaper event", evt=event)

        model = self._translation.schema_to_model(schema=event)

        try:
            self._db.add(model)

            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to insert diaper event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Diaper event inserted successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def get_diaper_event(self, event_id: str) -> schemas.DiaperEvent:
        """Retrieve a diaper event by its ID."""
        self._log.debug("Retrieving diaper event", event_id=event_id)

        model = (
            self._db.query(models.DiaperEvent)
            .filter(models.DiaperEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Diaper event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Diaper event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self._log.debug("Diaper event retrieved successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def list_diaper_events(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[schemas.DiaperEvent]:
        """List diaper events with pagination."""
        self._log.debug("Listing diaper events", limit=limit, offset=offset)

        models_list = (
            self._db.query(models.DiaperEvent)
            .order_by(models.DiaperEvent.time_start.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not models_list:
            self._log.info("No diaper events found")
            return []
        self._log.debug("Diaper events listed successfully", count=len(models_list))

        return [self._translation.model_to_schema(model=model) for model in models_list]

    def update_diaper_event(
        self, event_id: str, event: schemas.DiaperEvent
    ) -> schemas.DiaperEvent:
        """Update an existing diaper event."""
        self._log.debug("Updating diaper event", event_id=event_id, evt=event)

        try:
            model = (
                self._db.query(models.DiaperEvent)
                .filter(models.DiaperEvent.id == event_id)
                .first()
            )
        except LookupError as e:
            self._log.error("Invalid event type", error=repr(e))
            raise HTTPException(
                detail=f"Invalid event type for ID {event_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            self._log.error("Diaper event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Diaper event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        for key, value in event.model_dump().items():
            if key != "id":  # Avoid changing the ID
                set_attribute(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to update diaper event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Diaper event updated successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def delete_diaper_event(self, event_id: str) -> None:
        """Delete a diaper event by its ID."""
        self._log.debug("Deleting diaper event", event_id=event_id)

        model = (
            self._db.query(models.DiaperEvent)
            .filter(models.DiaperEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Diaper event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Diaper event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self._log.error("Failed to delete diaper event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Diaper event deleted successfully", event_id=event_id)

        return None
