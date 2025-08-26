from pydantic import Field
from events.schemas import Event
from events.schemas import EventType
from enum import Enum


class DiaperType(str, Enum):
    """Types of diaper changes."""

    PEE = "pee"
    POOP = "poop"
    BOTH = "both"


class DiaperContentsColor(str, Enum):
    """Colors of diaper poop."""

    YELLOW = "yellow"
    BROWN = "brown"
    GREEN = "green"
    BLACK = "black"


class DiaperContentsConsistency(str, Enum):
    """Consistency of diaper poop."""

    WATERY = "watery"
    PASTY = "pasty"


class DiaperContentsSize(str, Enum):
    """Size of diaper poop."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class DiaperEvent(Event):
    """Event for diaper changes."""

    name: EventType = Field(default=EventType.DIAPER_CHANGE, frozen=True)
    description: str = Field(default="Diaper change event", frozen=True)

    diaper_type: DiaperType
    diaper_contents_color: DiaperContentsColor | None = None
    diaper_contents_consistency: DiaperContentsConsistency | None = None
    diaper_contents_size: DiaperContentsSize | None = None
