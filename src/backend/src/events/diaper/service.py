from typing import Sequence
from common.service import CommonService
from sqlalchemy.orm import Session
from events.diaper.model_schema_translation import DiaperModelSchemaTranslation
from events.diaper import schemas
from ulid import ULID
from events.diaper.persistence import DiaperPersistence


class DiaperService(CommonService):
    """Service for handling diaper-related operations."""

    def __init__(self, db: Session):
        """
        Initialize the DiaperService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__(db)
        self._translation = DiaperModelSchemaTranslation()
        self._persistence = DiaperPersistence(db=db)

    def create_diaper_event(self, event: schemas.DiaperEvent) -> schemas.DiaperEvent:
        """Create a new diaper event."""

        self._log.debug("Creating diaper event", evt=event)

        event.id = str(ULID())

        inserted_event = self._persistence.insert_diaper_event(event=event)

        return inserted_event

    def get_diaper_event(self, event_id: str) -> schemas.DiaperEvent:
        """Retrieve a diaper event by its ID."""
        self._log.debug("Retrieving diaper event", event_id=event_id)

        return self._persistence.get_diaper_event(event_id=event_id)

    def list_diaper_events(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[schemas.DiaperEvent]:
        """List diaper events with pagination."""
        self._log.debug("Listing diaper events", limit=limit, offset=offset)

        return self._persistence.list_diaper_events(limit=limit, offset=offset)

    def update_diaper_event(
        self, event_id: str, event: schemas.DiaperEvent
    ) -> schemas.DiaperEvent:
        """Update an existing diaper event."""
        self._log.debug("Updating diaper event", event_id=event_id, evt=event)

        return self._persistence.update_diaper_event(event_id=event_id, event=event)

    def delete_diaper_event(self, event_id: str) -> None:
        """Delete a diaper event by its ID."""
        self._log.debug("Deleting diaper event", event_id=event_id)

        self._persistence.delete_diaper_event(event_id=event_id)

        self._log.debug("Diaper event deleted successfully", event_id=event_id)

        return None
