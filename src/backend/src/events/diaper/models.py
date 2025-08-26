from events import models
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from events.schemas import EventType
from events.diaper.schemas import (
    DiaperType,
    DiaperContentsColor,
    DiaperContentsConsistency,
    DiaperContentsSize,
)


class DiaperEvent(models.Event):
    """Event for diaper changes."""

    __tablename__ = "diaper_events"

    id: Mapped[str] = mapped_column(ForeignKey("events.id"), primary_key=True)
    diaper_type: Mapped[DiaperType] = mapped_column(Enum(DiaperType), nullable=False)
    diaper_contents_color: Mapped[DiaperContentsColor] = mapped_column(
        Enum(DiaperContentsColor), nullable=True
    )
    diaper_contents_consistency: Mapped[DiaperContentsConsistency] = mapped_column(
        Enum(DiaperContentsConsistency), nullable=True
    )
    diaper_contents_size: Mapped[DiaperContentsSize] = mapped_column(
        Enum(DiaperContentsSize), nullable=True
    )

    __mapper_args__ = {"polymorphic_identity": EventType.DIAPER_CHANGE.value}

    def __repr__(self):
        return f"<DiaperEvent(id={self.id}, type={self.diaper_type})>"

    def __str__(self):
        return f"DiaperEvent {self.id} of type {self.diaper_type}"
