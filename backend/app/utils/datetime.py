from datetime import datetime


def now() -> datetime:
    return datetime.now()


def to_naive(value: datetime) -> datetime:
    if value.tzinfo is not None:
        value = value.replace(tzinfo=None)
    return value
