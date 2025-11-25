from pydantic import AwareDatetime, BaseModel


class BottleFeedStatistic(BaseModel):
    time: AwareDatetime
    amount_ml: float
    time_since_last_feed_minutes: float


class DiaperStatistics(BaseModel):
    """Comprehensive diaper statistics for a given time window."""

    window_days: int
    total_diapers: int
    wet_only: int
    poop_only: int
    both: int

    # All days (including days with 0 diapers)
    avg_per_day: float
    median_per_day: float
    avg_wet_per_day: float
    avg_poop_per_day: float

    # Active days only (days with at least 1 diaper logged)
    days_with_diapers: int
    avg_per_active_day: float
    median_per_active_day: float

    # Range
    min_per_day: int
    max_per_day: int
