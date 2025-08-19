from pydantic import BaseModel, AwareDatetime
from enum import Enum


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
