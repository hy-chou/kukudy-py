from datetime import datetime, timezone


def get_ts():
    return datetime.now(timezone.utc).isoformat()[:19].replace(':', '.')
