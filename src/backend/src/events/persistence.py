from typing import Optional, Sequence
from sqlalchemy.orm import Session
from structlog import get_logger
from events.model_schema_translation import EventModelSchemaTranslation
from events import schemas, models
from fastapi import HTTPException, status
from sqlalchemy.orm.attributes import set_attribute
import datetime


class EventPersistence:
    def __init__(self, db: Session):
        self._log = get_logger()
        self._db = db
        self._translation = EventModelSchemaTranslation()

    def insert_event(self, event: schemas.Event) -> schemas.Event:
        """Insert a new event into the database."""
        self._log.debug("Inserting event", evt=event)

        model = self._translation.event_schema_to_model(schema=event)

        try:
            self._db.add(model)

            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to insert event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Event inserted successfully", model=model)

        return self._translation.event_model_to_schema(model=model)

    def get_event(self, event_id: str) -> schemas.Event:
        """Retrieve a event by its ID."""
        self._log.debug("Retrieving event", event_id=event_id)

        model = self._db.query(models.Event).filter(models.Event.id == event_id).first()

        if not model:
            self._log.error("Event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self._log.debug("Event retrieved successfully", model=model)

        return self._translation.event_model_to_schema(model=model)

    def list_events(
        self,
        limit: int = 100,
        offset: int = 0,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
    ) -> tuple[int, Sequence[schemas.Event]]:
        """List events with pagination and time window filtering."""
        self._log.debug(
            "Listing events",
            limit=limit,
            offset=offset,
            start_time=start_time,
            end_time=end_time,
        )

        query = self._db.query(models.Event)

        if start_time:
            query = query.filter(models.Event.time_start >= start_time)

        if end_time:
            query = query.filter(models.Event.time_start <= end_time)

        total = query.count()

        models_list = (
            query.order_by(models.Event.time_start.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not models_list:
            self._log.info("No events found")
            return 0, []
        self._log.debug("Events listed successfully", count=len(models_list))

        return total, [
            self._translation.event_model_to_schema(model=model)
            for model in models_list
        ]

    def update_event(self, event_id: str, event: schemas.Event) -> schemas.Event:
        """Update an existing event."""
        self._log.debug("Updating event", event_id=event_id, evt=event)

        try:
            model = (
                self._db.query(models.Event).filter(models.Event.id == event_id).first()
            )
        except LookupError as e:
            self._log.error("Invalid event type", error=repr(e))
            raise HTTPException(
                detail=f"Invalid event type for ID {event_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not model:
            self._log.error("Event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        for key, value in event.model_dump().items():
            if key != "id":  # Avoid changing the ID
                set_attribute(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self._log.error("Failed to update event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Event updated successfully", model=model)

        return self._translation.event_model_to_schema(model=model)

    def delete_event(self, event_id: str) -> None:
        """Delete a event by its ID."""
        self._log.debug("Deleting event", event_id=event_id)

        model = self._db.query(models.Event).filter(models.Event.id == event_id).first()

        if not model:
            self._log.error("Event not found", event_id=event_id)
            raise HTTPException(
                detail=f"Event with ID {event_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self._log.error("Failed to delete event", error=repr(e))
            self._db.rollback()
            raise

        self._log.debug("Event deleted successfully", event_id=event_id)

        return None
