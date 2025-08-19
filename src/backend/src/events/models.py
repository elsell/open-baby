from events.schemas import EventType
from persistence.database import Base
from datetime import datetime
from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column


class Event(Base):
    """Base event with shared fields between all baby events."""

    __tablename__ = "events"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[EventType] = mapped_column(Enum(EventType), index=True)
    description: Mapped[str] = mapped_column(index=True)
    time_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    time_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_on": name,
        "polymorphic_identity": EventType.__base__,
    }

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name}, time_start={self.time_start})>"

    def __str__(self):
        return f"Event {self.name} at {self.time_start}"
