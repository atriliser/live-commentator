from live_commentator import players
from live_commentator.player import Player


def test_find_player_negative() -> None:
    assert players.find_player("Ronaldinho") is None


def test_find_player_positive() -> None:
    assert players.find_player("Ronaldo") == Player(position="forward", number=11)


def test_players_by_position() -> None:
    res = players.players_by_position("forward")

    assert res == ["Ronaldo"]
