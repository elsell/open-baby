"""Translation of model schemas for diaper events."""

from events.diaper import schemas, models
import datetime


class DiaperModelSchemaTranslation:
    """Translation between diaper event models and schemas."""

    @staticmethod
    def model_to_schema(model: models.DiaperEvent) -> schemas.DiaperEvent:
        """Convert DiaperEvent model to DiaperEvent schema."""
        return schemas.DiaperEvent(
            id=model.id,
            description=model.description,
            time_start=model.time_start.replace(tzinfo=datetime.UTC),
            time_end=model.time_end.replace(tzinfo=datetime.UTC)
            if model.time_end
            else None,
            notes=model.notes,
            diaper_type=schemas.DiaperType(model.diaper_type),
            diaper_contents_color=schemas.DiaperContentsColor(
                model.diaper_contents_color
            )
            if model.diaper_contents_color
            else None,
            diaper_contents_consistency=schemas.DiaperContentsConsistency(
                model.diaper_contents_consistency
            )
            if model.diaper_contents_consistency
            else None,
            diaper_contents_size=schemas.DiaperContentsSize(model.diaper_contents_size)
            if model.diaper_contents_size
            else None,
        )

    @staticmethod
    def schema_to_model(schema: schemas.DiaperEvent) -> models.DiaperEvent:
        """Convert DiaperEvent schema to DiaperEvent model."""
        return models.DiaperEvent(
            id=schema.id,
            description=schema.description,
            time_start=schema.time_start.replace(tzinfo=datetime.UTC),
            time_end=schema.time_end.replace(tzinfo=datetime.UTC)
            if schema.time_end
            else None,
            notes=schema.notes,
            diaper_type=schema.diaper_type,
            diaper_contents_color=schema.diaper_contents_color,
            diaper_contents_consistency=schema.diaper_contents_consistency,
            diaper_contents_size=schema.diaper_contents_size,
        )
