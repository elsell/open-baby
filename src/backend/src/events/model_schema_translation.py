"""Translation of model schemas for events."""

from events import schemas, models
import datetime


class EventModelSchemaTranslation:
    """Translation between event models and schemas."""

    @staticmethod
    def event_model_to_schema(
        model: models.Event,
    ) -> schemas.Event:
        """Convert Event model to Event schema."""
        return schemas.Event(
            id=model.id,
            name=model.name,
            description=model.description,
            time_start=model.time_start.replace(tzinfo=datetime.UTC),
            time_end=model.time_end.replace(tzinfo=datetime.UTC)
            if model.time_end
            else None,
            notes=model.notes,
        )

    @staticmethod
    def event_schema_to_model(
        schema: schemas.Event,
    ) -> models.Event:
        """Convert Event schema to Event model."""
        return models.Event(
            id=schema.id,
            name=schema.name,
            description=schema.description,
            time_start=schema.time_start.replace(tzinfo=None),
            time_end=schema.time_end.replace(tzinfo=None) if schema.time_end else None,
            notes=schema.notes,
        )
