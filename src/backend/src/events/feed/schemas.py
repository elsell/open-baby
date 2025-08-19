from pydantic import Field
from events.schemas import Event
from enum import Enum
from events.schemas import EventType


class BreastSide(str, Enum):
    """Enum for breast feeding side."""

    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class FeedBottleEvent(Event):
    """Event for bottle feeding."""

    name: EventType = Field(default=EventType.FEED_BOTTLE, frozen=True)
    description: str = Field(default="Bottle feeding event", frozen=True)

    amount_ml: int
    is_formula: bool  # True if formula, false if breast milk


class FeedBreastEvent(Event):
    """Event for breastfeeding."""

    name: EventType = Field(default=EventType.FEED_BREAST, frozen=True)
    description: str = Field(default="Breastfeeding event", frozen=True)

    side: BreastSide = BreastSide.BOTH
