import datetime
from typing import Sequence
from collections import defaultdict

from pydantic import AwareDatetime
from common.service import CommonService
from sqlalchemy.orm import Session
from stats.persistence import StatsPersistence
from stats import schemas
from events.diaper.schemas import DiaperType


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

    def get_diaper_statistics(
        self, days: int, end_date: AwareDatetime | None
    ) -> schemas.DiaperStatistics:
        """Get comprehensive diaper statistics for a given time window."""
        self._log.debug("Getting diaper statistics", days=days, end_date=end_date)

        # Calculate date range
        if end_date is None:
            end_date = datetime.datetime.now(datetime.UTC)
        start_date = end_date - datetime.timedelta(days=days)

        # Get diaper events
        events = self._persistence.get_diaper_events(
            start_date=start_date, end_date=end_date
        )

        # Count by type
        wet_only = sum(1 for e in events if e.diaper_type == DiaperType.PEE)
        poop_only = sum(1 for e in events if e.diaper_type == DiaperType.POOP)
        both = sum(1 for e in events if e.diaper_type == DiaperType.BOTH)
        total_diapers = len(events)

        # Group by day
        diapers_per_day: dict = defaultdict(int)
        wet_per_day_counts: dict = defaultdict(int)
        poop_per_day_counts: dict = defaultdict(int)

        for event in events:
            day_key = event.time_start.date()
            diapers_per_day[day_key] += 1

            # Count wet diapers (pee or both)
            if event.diaper_type in [DiaperType.PEE, DiaperType.BOTH]:
                wet_per_day_counts[day_key] += 1

            # Count poop diapers (poop or both)
            if event.diaper_type in [DiaperType.POOP, DiaperType.BOTH]:
                poop_per_day_counts[day_key] += 1

        # Calculate statistics for all days
        daily_counts = list(diapers_per_day.values())
        days_with_diapers = len(daily_counts)

        # All days average (including zero days)
        avg_per_day = total_diapers / days if days > 0 else 0

        # Calculate wet and poop averages
        total_wet = sum(wet_per_day_counts.values())
        total_poop = sum(poop_per_day_counts.values())
        avg_wet_per_day = total_wet / days if days > 0 else 0
        avg_poop_per_day = total_poop / days if days > 0 else 0

        # Median for all days (including zero days)
        all_days_list = [
            diapers_per_day.get(start_date.date() + datetime.timedelta(days=i), 0)
            for i in range(days)
        ]
        median_per_day = self._calculate_median(all_days_list)

        # Active days statistics
        avg_per_active_day = (
            sum(daily_counts) / len(daily_counts) if daily_counts else 0
        )
        median_per_active_day = self._calculate_median(daily_counts)

        # Range
        min_per_day = min(all_days_list) if all_days_list else 0
        max_per_day = max(all_days_list) if all_days_list else 0

        return schemas.DiaperStatistics(
            window_days=days,
            total_diapers=total_diapers,
            wet_only=wet_only,
            poop_only=poop_only,
            both=both,
            avg_per_day=round(avg_per_day, 2),
            median_per_day=median_per_day,
            avg_wet_per_day=round(avg_wet_per_day, 2),
            avg_poop_per_day=round(avg_poop_per_day, 2),
            days_with_diapers=days_with_diapers,
            avg_per_active_day=round(avg_per_active_day, 2),
            median_per_active_day=median_per_active_day,
            min_per_day=min_per_day,
            max_per_day=max_per_day,
        )

    def _calculate_median(self, values: list[int]) -> float:
        """Calculate median from a list of integers."""
        if not values:
            return 0
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        else:
            return float(sorted_values[n // 2])
