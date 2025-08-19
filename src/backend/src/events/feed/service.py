from common.service import CommonService
from sqlalchemy.orm import Session
from events.feed.model_schema_translation import FeedModelSchemaTranslation
from events.feed import schemas
from ulid import ULID
from events.feed.persistence import FeedPersistence


class FeedService(CommonService):
    """Service for handling feed-related operations."""

    def __init__(self, db: Session):
        """
        Initialize the FeedService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__(db)
        self._translation = FeedModelSchemaTranslation()
        self._persistence = FeedPersistence(db=db)

    def create_bottle_feed_event(
        self, event: schemas.FeedBottleEvent
    ) -> schemas.FeedBottleEvent:
        """Create a new bottle feed event."""

        self._log.debug("Creating bottle feed event", evt=event)

        event.id = str(ULID())

        inserted_event = self._persistence.insert_bottle_feed_event(event=event)

        return inserted_event

    def get_bottle_feed_event(self, event_id: str) -> schemas.FeedBottleEvent:
        """Retrieve a bottle feed event by its ID."""
        self._log.debug("Retrieving bottle feed event", event_id=event_id)

        return self._persistence.get_bottle_feed_event(event_id=event_id)

    def update_bottle_feed_event(
        self, event_id: str, event: schemas.FeedBottleEvent
    ) -> schemas.FeedBottleEvent:
        """Update an existing bottle feed event."""
        self._log.debug("Updating bottle feed event", event_id=event_id, evt=event)

        return self._persistence.update_bottle_feed_event(
            event_id=event_id, event=event
        )

    def delete_bottle_feed_event(self, event_id: str) -> None:
        """Delete a bottle feed event by its ID."""
        self._log.debug("Deleting bottle feed event", event_id=event_id)

        self._persistence.delete_bottle_feed_event(event_id=event_id)

    def create_breast_feed_event(
        self, event: schemas.FeedBreastEvent
    ) -> schemas.FeedBreastEvent:
        """Create a new breast feed event."""
        self._log.debug("Creating breast feed event", evt=event)

        event.id = str(ULID())

        inserted_event = self._persistence.insert_breast_feed_event(event=event)

        return inserted_event

    def get_breast_feed_event(self, event_id: str) -> schemas.FeedBreastEvent:
        """Retrieve a breast feed event by its ID."""
        self._log.debug("Retrieving breast feed event", event_id=event_id)

        return self._persistence.get_breast_feed_event(event_id=event_id)

    def update_breast_feed_event(
        self, event_id: str, event: schemas.FeedBreastEvent
    ) -> schemas.FeedBreastEvent:
        """Update an existing breast feed event."""
        self._log.debug("Updating breast feed event", event_id=event_id, evt=event)

        return self._persistence.update_breast_feed_event(
            event_id=event_id, event=event
        )

    def delete_breast_feed_event(self, event_id: str) -> None:
        """Delete a breast feed event by its ID."""
        self._log.debug("Deleting breast feed event", event_id=event_id)

        self._persistence.delete_breast_feed_event(event_id=event_id)

        self._log.debug("Breast feed event deleted successfully", event_id=event_id)

        return None
