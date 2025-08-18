from persistence.database import Base
from sqlalchemy import Column, String, DateTime


class Event(Base):
    """Base event with shared fields between all baby events."""

    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name}, time_start={self.time_start})>"

    def __str__(self):
        return f"Event {self.name} at {self.time_start}"
