from events.schemas import Event
from enum import Enum


class BreastSide(str, Enum):
    """Enum for breast feeding side."""

    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class FeedBottleEvent(Event):
    """Event for bottle feeding."""

    amount_ml: int
    is_formula: bool  # True if formula, false if breast milk


class FeedBreastEvent(Event):
    """Event for breastfeeding."""

    side: BreastSide = BreastSide.BOTH
