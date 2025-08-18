from persistence.database import Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped
from events.models import Event


class FeedBottleEvent(Base):
    """Event for bottle feeding."""

    __tablename__ = "bottle_feed_events"

    id = Column(String, ForeignKey("events.id"), primary_key=True)
    amount_ml = Column(String, nullable=False)
    is_formula = Column(Boolean, nullable=False)

    # relationship with the Event base class
    event: Mapped[Event] = relationship("Event")


class FeedBreastEvent(Base):
    """Event for breastfeeding."""

    __tablename__ = "breast_feed_events"

    id = Column(String, ForeignKey("events.id"), primary_key=True)
    side = Column(String, nullable=False)  # Use enum or string for side

    event: Mapped[Event] = relationship("Event")

    def __repr__(self):
        return f"<BreastFeedEvent(id={self.id}, side={self.side})>"

    def __str__(self):
        return f"BreastFeedEvent {self.id} on {self.side} side"
