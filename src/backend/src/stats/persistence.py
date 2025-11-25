from typing import Sequence
from sqlalchemy.orm import Session
from structlog import get_logger
from events.feed.models import FeedBottleEvent
from events.diaper.models import DiaperEvent
from datetime import datetime


class StatsPersistence:
    def __init__(self, db: Session):
        self._log = get_logger()
        self._db = db

    def get_bottle_feed_events(
        self, start_date: datetime | None, end_date: datetime | None
    ) -> Sequence[FeedBottleEvent]:
        """Retrieve bottle feed events within a date range."""
        self._log.debug(
            "Retrieving bottle feed events for stats",
            start_date=start_date,
            end_date=end_date,
        )

        query = self._db.query(FeedBottleEvent)

        if start_date:
            query = query.filter(FeedBottleEvent.time_start >= start_date)
        if end_date:
            query = query.filter(FeedBottleEvent.time_start <= end_date)

        models_list = query.order_by(FeedBottleEvent.time_start.asc()).all()

        if not models_list:
            self._log.info("No bottle feed events found for stats")
            return []

        self._log.debug(
            "Bottle feed events for stats retrieved successfully",
            count=len(models_list),
        )

        return models_list

    def get_diaper_events(
        self, start_date: datetime | None, end_date: datetime | None
    ) -> Sequence[DiaperEvent]:
        """Retrieve diaper events within a date range."""
        self._log.debug(
            "Retrieving diaper events for stats",
            start_date=start_date,
            end_date=end_date,
        )

        query = self._db.query(DiaperEvent)

        if start_date:
            query = query.filter(DiaperEvent.time_start >= start_date)
        if end_date:
            query = query.filter(DiaperEvent.time_start <= end_date)

        models_list = query.order_by(DiaperEvent.time_start.asc()).all()

        if not models_list:
            self._log.info("No diaper events found for stats")
            return []

        self._log.debug(
            "Diaper events for stats retrieved successfully",
            count=len(models_list),
        )

        return models_list
