from datetime import date, datetime, time, timedelta


def week_bounds(reference: datetime) -> tuple[datetime, datetime]:
    day_start = reference.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = day_start - timedelta(days=reference.weekday())
    sunday_end = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return monday, sunday_end


def overlaps_any(
    start: datetime,
    end: datetime,
    intervals: list[tuple[datetime, datetime]],
) -> bool:
    for occupied_start, occupied_end in intervals:
        if start < occupied_end and occupied_start < end:
            return True
    return False


def combine_date_time(day: date, value: time | timedelta) -> datetime:
    base = datetime.combine(day, time(0, 0))
    if isinstance(value, timedelta):
        return base + value
    return base + timedelta(
        hours=value.hour,
        minutes=value.minute,
        seconds=value.second,
    )
