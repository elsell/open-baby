from events import models, schemas


class EventModelSchemaTranslation:
    """Translation of model schemas for events."""

    @staticmethod
    def event_model_to_schema(
        model: models.Event,
    ) -> schemas.Event:
        """Convert Event model to Event schema."""
        return schemas.Event(
            id=str(model.id),
            name=str(model.name),
            description=str(model.description),
            time_start=model.time_start,  # type: ignore
            time_end=model.time_end,  # type: ignore
            notes=str(model.notes),
        )

    @staticmethod
    def event_schema_to_model(
        schema: schemas.Event,
    ) -> models.Event:
        """Convert Event schema to Event model."""
        return models.Event(
            id=str(schema.id),
            name=schema.name,
            description=schema.description,
            time_start=schema.time_start,
            time_end=schema.time_end,
            notes=schema.notes,
        )
