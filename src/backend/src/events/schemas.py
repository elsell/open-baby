from pydantic import BaseModel, AwareDatetime
from enum import Enum
from typing import Any, Optional, Sequence


class EventType(str, Enum):
    """Enum for event types."""

    FEED_BOTTLE = "feed_bottle"
    FEED_BREAST = "feed_breast"


class Event(BaseModel):
    """Base event with shared fields between all baby events."""

    id: str
    name: EventType
    description: str
    time_start: AwareDatetime
    time_end: AwareDatetime | None = None
    notes: str | None = None


class EventWithMetadataResponse(BaseModel):
    """Pydantic model for API responses"""

    id: str
    name: str
    description: str
    time_start: AwareDatetime
    time_end: Optional[AwareDatetime] = None
    notes: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Response model for a list of events with total count."""

    total: int
    events: Sequence[EventWithMetadataResponse]
