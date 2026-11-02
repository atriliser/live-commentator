from pydantic import BaseModel, Field


class IdName(BaseModel):
    id: int
    name: str


class BaseEvent(BaseModel):
    id: str
    type: IdName
    team: IdName
    index: int
    period: int
    timestamp: str
    minute: int
    second: int
    possession_team: IdName
    possession: int
    play_pattern: IdName
    player: IdName | None = None
    location: tuple[float, float] | None = None
    position: IdName | None = None
    under_pressure: bool = False
    related_events: list[str] = []
    duration: float | None = None


class LineupEntry(BaseModel):
    player: IdName
    position: IdName
    jersey_number: int


class Tactics(BaseModel):
    formation: int
    lineup: list[LineupEntry]


class StartingXIEvent(BaseEvent):
    tactics: Tactics


class PassDetails(BaseModel):
    recipient: IdName | None = None
    length: float
    angle: float
    end_location: tuple[float, float]
    height: IdName
    outcome: IdName | None = None


class PassEvent(BaseEvent):
    player: IdName
    position: IdName
    location: tuple[float, float]
    pass_: PassDetails = Field(alias="pass")
