from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag

KNOWN_EVENT_TYPES = {"Starting XI", "Pass"}


class IdName(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: int
    name: str


class BaseEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
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
    model_config = ConfigDict(frozen=True)
    player: IdName
    position: IdName
    jersey_number: int


class Tactics(BaseModel):
    model_config = ConfigDict(frozen=True)
    formation: int
    lineup: list[LineupEntry]


class StartingXIEvent(BaseEvent):
    model_config = ConfigDict(frozen=True)
    tactics: Tactics


class PassDetails(BaseModel):
    model_config = ConfigDict(frozen=True)
    recipient: IdName | None = None
    length: float
    angle: float
    end_location: tuple[float, float]
    height: IdName
    outcome: IdName | None = None


class PassEvent(BaseEvent):
    model_config = ConfigDict(frozen=True)
    player: IdName
    position: IdName
    location: tuple[float, float]
    pass_: PassDetails = Field(alias="pass")


def event_type_name(v: Any) -> str | None:
    type_name = v["type"]["name"]
    if isinstance(type_name, str):
        return type_name
    return None


def event_tag(v: Any) -> str | None:
    type_name = event_type_name(v)
    if type_name is None:
        return None
    if type_name in KNOWN_EVENT_TYPES:
        return type_name
    return "other"


StatsBombEvent = Annotated[
    Annotated[PassEvent, Tag("Pass")]
    | Annotated[StartingXIEvent, Tag("Starting XI")]
    | Annotated[BaseEvent, Tag("other")],
    Discriminator(event_tag),
]
