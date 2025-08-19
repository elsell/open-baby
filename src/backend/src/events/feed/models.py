from events import models
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from events.schemas import EventType


class FeedBottleEvent(models.Event):
    """Event for bottle feeding."""

    __tablename__ = "bottle_feed_events"

    id: Mapped[str] = mapped_column(ForeignKey("events.id"), primary_key=True)
    amount_ml: Mapped[int] = mapped_column(nullable=False)
    is_formula: Mapped[bool] = mapped_column(nullable=False)

    __mapper_args__ = {"polymorphic_identity": EventType.FEED_BOTTLE.value}

    def __repr__(self):
        return f"<BottleFeedEvent(id={self.id}, amount_ml={self.amount_ml}, is_formula={self.is_formula})>"

    def __str__(self):
        return f"BottleFeedEvent {self.id} with {self.amount_ml} ml, formula: {self.is_formula}"


class FeedBreastEvent(models.Event):
    """Event for breastfeeding."""

    __tablename__ = "breast_feed_events"

    id: Mapped[str] = mapped_column(ForeignKey("events.id"), primary_key=True)
    side: Mapped[str] = mapped_column(nullable=False)  # Use enum or string for side

    __mapper_args__ = {"polymorphic_identity": EventType.FEED_BREAST.value}

    def __repr__(self):
        return f"<BreastFeedEvent(id={self.id}, side={self.side})>"

    def __str__(self):
        return f"BreastFeedEvent {self.id} on {self.side} side"
