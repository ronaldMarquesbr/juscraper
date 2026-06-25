from datetime import datetime


def parse_iso_timestamp_to_date(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()
