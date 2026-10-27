PLAYERS = {"Modric": "defender",
           "Ronaldo": "forward",
           "Messi": "capitain"}

def find_player(name: str) -> str | None:
    return PLAYERS.get(name)

def check_player() -> str:
    position = find_player("Messi")

    if not position is None:
        return "Position is:" + position.upper()
    else: return "Not found"