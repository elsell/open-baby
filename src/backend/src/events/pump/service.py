from typing import Sequence
from common.service import CommonService
from sqlalchemy.orm import Session
from events.pump.model_schema_translation import PumpModelSchemaTranslation
from events.pump import schemas
from ulid import ULID
from events.pump.persistence import PumpPersistence


class PumpService(CommonService):
    """Service for handling pump-related operations."""

    def __init__(self, db: Session):
        """
        Initialize the PumpService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__(db)
        self._translation = PumpModelSchemaTranslation()
        self._persistence = PumpPersistence(db=db)

    def create_pump_event(self, event: schemas.PumpEvent) -> schemas.PumpEvent:
        """Create a new pump event."""

        self._log.debug("Creating pump event", evt=event)

        event.id = str(ULID())

        inserted_event = self._persistence.insert_pump_event(event=event)

        return inserted_event

    def get_pump_event(self, event_id: str) -> schemas.PumpEvent:
        """Retrieve a pump event by its ID."""
        self._log.debug("Retrieving pump event", event_id=event_id)

        return self._persistence.get_pump_event(event_id=event_id)

    def list_pump_events(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[schemas.PumpEvent]:
        """List pump events with pagination."""
        self._log.debug("Listing pump events", limit=limit, offset=offset)

        return self._persistence.list_pump_events(limit=limit, offset=offset)

    def update_pump_event(
        self, event_id: str, event: schemas.PumpEvent
    ) -> schemas.PumpEvent:
        """Update an existing pump event."""
        self._log.debug("Updating pump event", event_id=event_id, evt=event)

        return self._persistence.update_pump_event(event_id=event_id, event=event)

    def delete_pump_event(self, event_id: str) -> None:
        """Delete a pump event by its ID."""
        self._log.debug("Deleting pump event", event_id=event_id)

        self._persistence.delete_pump_event(event_id=event_id)

        self._log.debug("Pump event deleted successfully", event_id=event_id)

        return None
