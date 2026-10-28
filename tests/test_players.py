from live_commentator import players


def test_find_player_negative():
    assert players.find_player("Ronaldinho") == None


def test_players_by_position():
    res = players.players_by_position("forward")

    assert res == ["Ronaldo"]
