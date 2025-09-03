from pydantic import Field
from events.schemas import Event
from events.schemas import EventType


class PumpEvent(Event):
    """Event for diaper changes."""

    name: EventType = Field(default=EventType.PUMP, frozen=True)
    description: str = Field(default="Pump event", frozen=True)

    amount_ml: float = Field(description="Amount pumped in milliliters", ge=0)
