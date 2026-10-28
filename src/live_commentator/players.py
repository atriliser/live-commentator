PLAYERS: dict[str, tuple[str, int]] = {
    "Modric": ("defender", 1),
    "Ronaldo": ("forward", 11),
    "Messi": ("midfielder", 8),
}


def find_player(name: str) -> tuple[str, int] | None:
    return PLAYERS.get(name)


def check_player() -> str:
    player = find_player("Messi")

    if player is None:
        return "Not found"

    return "Position is:" + player[0].upper()


def players_by_position(position: str) -> list[str]:
    players_names: list[str] = []
    for name, (pos, _) in PLAYERS.items():
        if position == pos:
            players_names.append(name)
    return players_names
