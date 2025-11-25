"""Router for statistics."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import AwareDatetime
from sqlalchemy.orm import Session
import structlog
from stats.service import StatsService
from stats import schemas
from persistence.dependencies import get_db

router = APIRouter()

log = structlog.get_logger()


@router.get("/feeds", response_model=list[schemas.BottleFeedStatistic])
def get_feed_statistic(
    start_date: Optional[AwareDatetime] = Query(
        None,
        description="Start date in ISO 8601 format (YYYY-MM-DD) or a full timestamp for precise filtering",
    ),
    end_date: Optional[AwareDatetime] = Query(
        None, description="End date in ISO 8601 format (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db),
):
    """Retrieve a feed statistic by its ID."""
    service = StatsService(db=db)
    return service.get_feed_statistic(start_date=start_date, end_date=end_date)


@router.get("/diapers", response_model=schemas.DiaperStatistics)
def get_diaper_statistics(
    days: int = Query(
        7,
        description="Number of days to include in the statistics window",
        ge=1,
    ),
    end_date: Optional[AwareDatetime] = Query(
        None,
        description="End date for the statistics window (defaults to now)",
    ),
    db: Session = Depends(get_db),
):
    """Retrieve comprehensive diaper statistics for a given time window."""
    service = StatsService(db=db)
    return service.get_diaper_statistics(days=days, end_date=end_date)
