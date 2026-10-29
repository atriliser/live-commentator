from live_commentator.player import Player

PLAYERS: dict[str, Player] = {
    "Modric": Player("defender", 1),
    "Ronaldo": Player("forward", 11),
    "Messi": Player("midfielder", 8),
}


def find_player(name: str) -> Player | None:
    return PLAYERS.get(name)


def check_player() -> str:
    player = find_player("Messi")

    if player is None:
        return "Not found"

    return "Position is:" + player.position.upper()


def players_by_position(position: str) -> list[str]:
    players_names: list[str] = []
    for name, player in PLAYERS.items():
        if position == player.position:
            players_names.append(name)
    return players_names
