from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    position: str
    number: int
