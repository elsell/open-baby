from typing import Sequence
from sqlalchemy.orm import Session
from structlog import get_logger
from events.pump.model_schema_translation import PumpModelSchemaTranslation
from events.pump import schemas, models
from fastapi import HTTPException, status
from sqlalchemy.orm.attributes import set_attribute


class PumpPersistence:
    def __init__(self, db: Session):
        self._log = get_logger()
        self._db = db
        self._translation = PumpModelSchemaTranslation()

    def insert_pump_event(self, event: schemas.PumpEvent) -> schemas.PumpEvent:
        """Insert a new pump event into the database."""
        self._log.debug("Inserting pump event", evt=event)

        model = self._translation.schema_to_model(schema=event)

        try:
            self._db.add(model)

            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to insert pump event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Pump event inserted successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def get_pump_event(self, event_id: str) -> schemas.PumpEvent:
        """Retrieve a pump event by its ID."""
        self._log.debug("Retrieving pump event", event_id=event_id)

        model = (
            self._db.query(models.PumpEvent)
            .filter(models.PumpEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Pump event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Pump event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self._log.debug("Pump event retrieved successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def list_pump_events(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[schemas.PumpEvent]:
        """List pump events with pagination."""
        self._log.debug("Listing pump events", limit=limit, offset=offset)

        models_list = (
            self._db.query(models.PumpEvent)
            .order_by(models.PumpEvent.time_start.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not models_list:
            self._log.info("No pump events found")
            return []
        self._log.debug("Pump events listed successfully", count=len(models_list))

        return [self._translation.model_to_schema(model=model) for model in models_list]

    def update_pump_event(
        self, event_id: str, event: schemas.PumpEvent
    ) -> schemas.PumpEvent:
        """Update an existing pump event."""
        self._log.debug("Updating pump event", event_id=event_id, evt=event)

        try:
            model = (
                self._db.query(models.PumpEvent)
                .filter(models.PumpEvent.id == event_id)
                .first()
            )
        except LookupError as e:
            self._log.error("Invalid event type", error=repr(e))
            raise HTTPException(
                detail=f"Invalid event type for ID {event_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            self._log.error("Pump event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Pump event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        for key, value in event.model_dump().items():
            if key != "id":  # Avoid changing the ID
                set_attribute(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to update pump event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Pump event updated successfully", model=model)

        return self._translation.model_to_schema(model=model)

    def delete_pump_event(self, event_id: str) -> None:
        """Delete a pump event by its ID."""
        self._log.debug("Deleting pump event", event_id=event_id)

        model = (
            self._db.query(models.PumpEvent)
            .filter(models.PumpEvent.id == event_id)
            .first()
        )

        if not model:
            self._log.error("Pump event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Pump event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self._log.error("Failed to delete pump event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Pump event deleted successfully", event_id=event_id)

        return None
