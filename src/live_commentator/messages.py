from pydantic import BaseModel, ConfigDict

from live_commentator.statsbomb.models import StatsBombEvent


class MatchEventMessage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    match_id: int
    event: StatsBombEvent
