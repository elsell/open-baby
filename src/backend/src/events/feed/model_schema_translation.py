"""Translation of model schemas for feed events."""

from events.feed import schemas, models


def bottle_feed_model_to_schema(
    model: models.BottleFeedEvent,
) -> schemas.FeedBottleEvent:
    """Convert BottleFeedEvent model to FeedBottleEvent schema."""
    return schemas.FeedBottleEvent(
        id=str(model.id),
        name=str(model.event.name),
        description=str(model.event.description),
        time_start=model.event.time_start,  # type: ignore
        time_end=model.event.time_end,  # type: ignore
        notes=str(model.event.notes),
        amount_ml=int(model.amount_ml),  # type: ignore
        is_formula=bool(model.is_formula),
    )


def bottle_feed_schema_to_model(
    schema: schemas.FeedBottleEvent,
) -> models.BottleFeedEvent:
    """Convert FeedBottleEvent schema to BottleFeedEvent model."""
    return models.BottleFeedEvent(
        id=str(schema.id),
        amount_ml=str(schema.amount_ml),
        is_formula=bool(schema.is_formula),
        event=models.Event(
            id=schema.id,
            name=schema.name,
            description=schema.description,
            time_start=schema.time_start,
            time_end=schema.time_end,
            notes=schema.notes,
        ),
    )


def breast_feed_model_to_schema(
    model: models.BreastFeedEvent,
) -> schemas.FeedBreastEvent:
    """Convert BreastFeedEvent model to FeedBreastEvent schema."""
    return schemas.FeedBreastEvent(
        id=str(model.id),
        name=str(model.event.name),
        description=str(model.event.description),
        time_start=model.event.time_start,  # type: ignore
        time_end=model.event.time_end,  # type: ignore
        notes=str(model.event.notes),
        side=schemas.BreastSide(model.side),
    )


def breast_feed_schema_to_model(
    schema: schemas.FeedBreastEvent,
) -> models.BreastFeedEvent:
    """Convert FeedBreastEvent schema to BreastFeedEvent model."""
    return models.BreastFeedEvent(
        id=str(schema.id),
        side=str(schema.side),
        event=models.Event(
            id=schema.id,
            name=schema.name,
            description=schema.description,
            time_start=schema.time_start,
            time_end=schema.time_end,
            notes=schema.notes,
        ),
    )
