from pydantic import AwareDatetime, BaseModel


class BottleFeedStatistic(BaseModel):
    time: AwareDatetime
    amount_ml: float
    time_since_last_feed_minutes: float
