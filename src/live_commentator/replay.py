from live_commentator.statsbomb.models import BaseEvent


def timestamp_to_seconds(timestamp: str) -> float:
    hours, minutes, seconds = timestamp.split(":")
    return int(hours) * 60 * 60 + int(minutes) * 60 + float(seconds)


def pause_seconds(prev: BaseEvent, curr: BaseEvent) -> float:
    if prev.period != curr.period:
        return 0.0
    return timestamp_to_seconds(curr.timestamp) - timestamp_to_seconds(prev.timestamp)
