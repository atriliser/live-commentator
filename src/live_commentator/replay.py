def timestamp_to_seconds(timestamp: str) -> float:
    hours, minutes, seconds = timestamp.split(":")
    return int(hours) * 60 * 60 + int(minutes) * 60 + float(seconds)
