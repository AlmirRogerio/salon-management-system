from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.config import settings

_tz = ZoneInfo(settings.timezone)


def now() -> datetime:
    return datetime.now(_tz).replace(tzinfo=None)


def to_naive(value: datetime) -> datetime:
    if value.tzinfo is not None:
        value = value.replace(tzinfo=None)
    return value
