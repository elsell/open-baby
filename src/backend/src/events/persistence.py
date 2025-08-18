from typing import Sequence
from sqlalchemy.orm import Session
from structlog import get_logger
from events.model_schema_translation import EventModelSchemaTranslation
from events import models, schemas


class EventPersistence:
    """Persistence for "Event" resource."""

    def __init__(self, db: Session):
        self.log = get_logger()
        self._db = db
        self._translation = EventModelSchemaTranslation()

    def insert_event(self, event: schemas.Event) -> models.Event:
        """Insert a new event into the database."""
        self.log.debug("Inserting event", evt=event)

        model = self._translation.event_schema_to_model(event)

        try:
            self._db.add(model)
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self.log.error("Failed to insert event", error=repr(e))
            self._db.rollback()
            raise

        self.log.debug("Event inserted successfully", model=model)

        return model

    def get_event(self, event_id: str) -> models.Event:
        """Retrieve an event by its ID."""
        self.log.debug("Retrieving event", event_id=event_id)

        model = self._db.query(models.Event).filter(models.Event.id == event_id).first()

        if not model:
            self.log.error("Event not found", event_id=event_id)
            raise ValueError(f"Event with ID {event_id} not found")

        self.log.debug("Event retrieved successfully", model=model)

        return model

    def update_event(self, event_id: str, event: schemas.Event) -> models.Event:
        """Update an existing event."""
        self.log.debug("Updating event", event_id=event_id, evt=event)

        model = self.get_event(event_id)
        updated_model = self._translation.event_schema_to_model(event)

        for key, value in updated_model.__dict__.items():
            if key != "id":  # Avoid changing the ID
                setattr(model, key, value)

        try:
            self._db.commit()
            self._db.refresh(model)
        except Exception as e:
            self.log.error("Failed to update event", error=repr(e))
            self._db.rollback()
            raise

        self.log("Event updated successfully", model=model)

        return model

    def delete_event(self, event_id: str) -> None:
        """Delete an event by its ID."""
        self.log.debug("Deleting event", event_id=event_id)

        model = self.get_event(event_id)

        try:
            self._db.delete(model)
            self._db.commit()
        except Exception as e:
            self.log.error("Failed to delete event", error=repr(e))
            self._db.rollback()
            raise

        self.log.debug("Event deleted successfully", event_id=event_id)

    def list_events(
        self,
        start: int = 0,
        limit: int = 100,
        sort_by: str = "time_start",
        sort_order: str = "asc",
    ) -> Sequence[schemas.Event]:
        """List all events."""
        self.log.debug("Listing all events")

        query = self._db.query(models.Event)

        if sort_order == "desc":
            query = query.order_by(getattr(models.Event, sort_by).desc())
        else:
            query = query.order_by(getattr(models.Event, sort_by).asc())

        events = query.offset(start).limit(limit).all()

        self.log.debug("Events listed successfully", count=len(events))

        return [self._translation.event_model_to_schema(event) for event in events]
