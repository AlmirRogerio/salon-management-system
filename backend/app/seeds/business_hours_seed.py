from datetime import time

from app.models import BusinessHours

DEFAULT_OPEN = time(8, 0)
DEFAULT_CLOSE = time(19, 0)
DEFAULT_SLOT_MINUTES = 30


async def seed_business_hours() -> None:
    for weekday in range(7):
        is_open = weekday != 6
        await BusinessHours.get_or_create(
            weekday=weekday,
            defaults={
                "is_open": is_open,
                "open_time": DEFAULT_OPEN,
                "close_time": DEFAULT_CLOSE,
                "slot_interval_minutes": DEFAULT_SLOT_MINUTES,
            },
        )
