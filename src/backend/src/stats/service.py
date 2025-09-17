import datetime
from typing import Sequence

from pydantic import AwareDatetime
from common.service import CommonService
from sqlalchemy.orm import Session
from stats.persistence import StatsPersistence
from stats import schemas


class StatsService(CommonService):
    """Service for handling statistics."""

    def __init__(self, db: Session):
        """
        Initialize the StatsService with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__(db)
        self._persistence = StatsPersistence(db=db)

    def get_feed_statistic(
        self, start_date: AwareDatetime | None, end_date: AwareDatetime | None
    ) -> Sequence[schemas.BottleFeedStatistic]:
        """Get feed statistics."""
        self._log.debug(
            "Getting feed statistic", start_date=start_date, end_date=end_date
        )

        events = self._persistence.get_bottle_feed_events(
            start_date=start_date, end_date=end_date
        )

        stats: list[schemas.BottleFeedStatistic] = []
        for i, event in enumerate(events):
            time_since_last = (
                (event.time_start - events[i - 1].time_start).total_seconds() / 60
                if i > 0
                else 0
            )
            stats.append(
                schemas.BottleFeedStatistic(
                    time=event.time_start.replace(tzinfo=datetime.UTC),
                    amount_ml=event.amount_ml,
                    time_since_last_feed_minutes=time_since_last,
                )
            )

        return stats
