from typing import Literal

from pydantic import Field
from events.schemas import Event
from enum import Enum


class BreastSide(str, Enum):
    """Enum for breast feeding side."""

    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class FeedBottleEvent(Event):
    """Event for bottle feeding."""

    name: Literal["feed_bottle"] = Field(default="feed_bottle", frozen=True)
    description: str = Field(default="Bottle feeding event", frozen=True)

    amount_ml: int
    is_formula: bool  # True if formula, false if breast milk


class FeedBreastEvent(Event):
    """Event for breastfeeding."""

    name: Literal["feed_breast"] = Field(default="feed_breast", frozen=True)
    description: str = Field(default="Breastfeeding event", frozen=True)

    side: BreastSide = BreastSide.BOTH
