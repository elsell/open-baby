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
