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
