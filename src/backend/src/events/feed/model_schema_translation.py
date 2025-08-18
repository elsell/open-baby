"""Translation of model schemas for feed events."""

from events.feed import schemas, models
from events.model_schema_translation import EventModelSchemaTranslation
import datetime


class FeedModelSchemaTranslation:
    """Translation between feed event models and schemas."""

    @staticmethod
    def bottle_feed_model_to_schema(
        model: models.FeedBottleEvent,
    ) -> schemas.FeedBottleEvent:
        """Convert BottleFeedEvent model to FeedBottleEvent schema."""
        return schemas.FeedBottleEvent(
            id=str(model.id),
            description=str(model.event.description),
            time_start=model.event.time_start.replace(tzinfo=datetime.UTC),  # type: ignore
            time_end=model.event.time_end.replace(tzinfo=datetime.UTC),  # type: ignore
            notes=str(model.event.notes),
            amount_ml=int(model.amount_ml),  # type: ignore
            is_formula=bool(model.is_formula),
        )

    @staticmethod
    def bottle_feed_schema_to_model(
        schema: schemas.FeedBottleEvent,
    ) -> models.FeedBottleEvent:
        """Convert FeedBottleEvent schema to BottleFeedEvent model."""
        return models.FeedBottleEvent(
            id=str(schema.id),
            amount_ml=str(schema.amount_ml),
            is_formula=bool(schema.is_formula),
            event=EventModelSchemaTranslation.event_schema_to_model(schema),
        )

    @staticmethod
    def breast_feed_model_to_schema(
        model: models.FeedBreastEvent,
    ) -> schemas.FeedBreastEvent:
        """Convert BreastFeedEvent model to FeedBreastEvent schema."""
        return schemas.FeedBreastEvent(
            id=str(model.id),
            description=str(model.event.description),
            time_start=model.event.time_start.replace(tzinfo=datetime.UTC),  # type: ignore
            time_end=model.event.time_end.replace(tzinfo=datetime.UTC),  # type: ignore
            notes=str(model.event.notes),
            side=schemas.BreastSide(model.side),
        )

    @staticmethod
    def breast_feed_schema_to_model(
        schema: schemas.FeedBreastEvent,
    ) -> models.FeedBreastEvent:
        """Convert FeedBreastEvent schema to BreastFeedEvent model."""
        return models.FeedBreastEvent(
            id=str(schema.id),
            side=str(schema.side),
            event=EventModelSchemaTranslation.event_schema_to_model(schema),
        )
