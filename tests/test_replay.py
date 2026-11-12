from live_commentator.replay import timestamp_to_seconds


def test_timestamp_to_seconds() -> None:
    assert timestamp_to_seconds("00:00:00.000") == 0
    assert timestamp_to_seconds("00:01:02.500") == 62.5
    assert timestamp_to_seconds("01:00:00.000") == 3600.0
