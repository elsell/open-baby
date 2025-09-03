"""Translation of model schemas for pump events."""

from events.pump import schemas, models
import datetime


class PumpModelSchemaTranslation:
    """Translation between pump event models and schemas."""

    @staticmethod
    def model_to_schema(model: models.PumpEvent) -> schemas.PumpEvent:
        """Convert PumpEvent model to PumpEvent schema."""
        return schemas.PumpEvent(
            id=model.id,
            description=model.description,
            time_start=model.time_start.replace(tzinfo=datetime.UTC),
            time_end=model.time_end.replace(tzinfo=datetime.UTC)
            if model.time_end
            else None,
            notes=model.notes,
            amount_ml=model.amount_ml,
        )

    @staticmethod
    def schema_to_model(schema: schemas.PumpEvent) -> models.PumpEvent:
        """Convert PumpEvent schema to PumpEvent model."""
        return models.PumpEvent(
            id=schema.id,
            description=schema.description,
            time_start=schema.time_start.replace(tzinfo=None),
            time_end=schema.time_end.replace(tzinfo=None) if schema.time_end else None,
            notes=schema.notes,
            amount_ml=schema.amount_ml,
        )
