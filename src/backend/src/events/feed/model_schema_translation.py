"""Translation of model schemas for feed events."""

from events.feed import schemas, models
import datetime


class FeedModelSchemaTranslation:
    """Translation between feed event models and schemas."""

    @staticmethod
    def bottle_feed_model_to_schema(
        model: models.FeedBottleEvent,
    ) -> schemas.FeedBottleEvent:
        """Convert BottleFeedEvent model to FeedBottleEvent schema."""
        return schemas.FeedBottleEvent(
            id=model.id,
            description=model.description,
            time_start=model.time_start.replace(tzinfo=datetime.UTC),
            time_end=model.time_end.replace(tzinfo=datetime.UTC)
            if model.time_end
            else None,
            notes=model.notes,
            amount_ml=model.amount_ml,
            is_formula=model.is_formula,
        )

    @staticmethod
    def bottle_feed_schema_to_model(
        schema: schemas.FeedBottleEvent,
    ) -> models.FeedBottleEvent:
        """Convert FeedBottleEvent schema to BottleFeedEvent model."""
        return models.FeedBottleEvent(
            id=schema.id,
            description=schema.description,
            time_start=schema.time_start.replace(tzinfo=datetime.UTC),
            time_end=schema.time_end.replace(tzinfo=datetime.UTC)
            if schema.time_end
            else None,
            notes=schema.notes,
            amount_ml=schema.amount_ml,
            is_formula=bool(schema.is_formula),
        )

    @staticmethod
    def breast_feed_model_to_schema(
        model: models.FeedBreastEvent,
    ) -> schemas.FeedBreastEvent:
        """Convert BreastFeedEvent model to FeedBreastEvent schema."""

        return schemas.FeedBreastEvent(
            id=model.id,
            description=model.description,
            time_start=model.time_start.replace(tzinfo=datetime.UTC),
            time_end=model.time_end.replace(tzinfo=datetime.UTC)
            if model.time_end
            else None,
            notes=model.notes,
            side=schemas.BreastSide(model.side),
        )

    @staticmethod
    def breast_feed_schema_to_model(
        schema: schemas.FeedBreastEvent,
    ) -> models.FeedBreastEvent:
        """Convert FeedBreastEvent schema to BreastFeedEvent model."""
        return models.FeedBreastEvent(
            id=schema.id,
            description=schema.description,
            time_start=schema.time_start.replace(tzinfo=datetime.UTC),
            time_end=schema.time_end.replace(tzinfo=datetime.UTC)
            if schema.time_end
            else None,
            notes=schema.notes,
            side=schema.side,
        )
