from events import models
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from events.schemas import EventType


class PumpEvent(models.Event):
    """Event for pump sessions."""

    __tablename__ = "pump_events"

    id: Mapped[str] = mapped_column(ForeignKey("events.id"), primary_key=True)
    amount_ml: Mapped[float] = mapped_column(nullable=False)

    __mapper_args__ = {"polymorphic_identity": EventType.PUMP.value}

    def __repr__(self):
        return f"<PumpEvent(id={self.id}, amount_ml={self.amount_ml})>"

    def __str__(self):
        return f"PumpEvent {self.id} with {self.amount_ml} ml"
