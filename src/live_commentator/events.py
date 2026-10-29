from pydantic import BaseModel


class EventType(BaseModel):
    id: int
    name: str


class MatchPlayer(BaseModel):
    id: int
    name: str


class MatchEvent(BaseModel):
    minute: int
    type: EventType
    player: MatchPlayer
    location: tuple[float, float]
