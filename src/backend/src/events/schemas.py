from typing import Literal
from pydantic import BaseModel, AwareDatetime


class Event(BaseModel):
    """Base event with shared fields between all baby events."""

    id: str
    name: Literal["feed_bottle"] | Literal["feed_breast"]
    description: str
    time_start: AwareDatetime
    time_end: AwareDatetime | None = None
    notes: str | None = None
