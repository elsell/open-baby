from typing import Optional
from common.service import CommonService
from sqlalchemy.orm import Session
from events.model_schema_translation import EventModelSchemaTranslation
from events import schemas
from ulid import ULID
from events.persistence import EventPersistence
import datetime


class EventService(CommonService):
    """Service for handling event-related operations."""

    def __init__(self, db: Session):
        """
        Initialize the EventService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__(db)
        self._translation = EventModelSchemaTranslation()
        self._persistence = EventPersistence(db=db)

    def create_event(self, event: schemas.Event) -> schemas.Event:
        """Create a new event."""

        self._log.debug("Creating event", evt=event)

        event.id = str(ULID())

        inserted_event = self._persistence.insert_event(event=event)

        return inserted_event

    def get_event(self, event_id: str) -> schemas.Event:
        """Retrieve a event by its ID."""
        self._log.debug("Retrieving event", event_id=event_id)

        return self._persistence.get_event(event_id=event_id)

    def list_events(
        self,
        limit: int = 100,
        offset: int = 0,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
    ) -> schemas.EventListResponse:
        """List events with pagination and time window filtering."""
        self._log.debug(
            "Listing events",
            limit=limit,
            offset=offset,
            start_time=start_time,
            end_time=end_time,
        )

        total, events = self._persistence.list_events(
            limit=limit, offset=offset, start_time=start_time, end_time=end_time
        )

        return schemas.EventListResponse(total=total, events=events)

    def update_event(self, event_id: str, event: schemas.Event) -> schemas.Event:
        """Update an existing event."""
        self._log.debug("Updating event", event_id=event_id, evt=event)

        return self._persistence.update_event(event_id=event_id, event=event)

    def delete_event(self, event_id: str) -> None:
        """Delete a event by its ID."""
        self._log.debug("Deleting event", event_id=event_id)

        self._persistence.delete_event(event_id=event_id)
