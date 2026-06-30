from datetime import datetime, timezone


def parse_iso_timestamp_to_date(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()


def parse_unix_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date()
