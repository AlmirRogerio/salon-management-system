from datetime import date, datetime, time, timedelta


def week_bounds(
    reference: datetime, not_before: datetime | None = None
) -> tuple[datetime, datetime]:
    day_start = reference.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = day_start - timedelta(days=reference.weekday())
    sunday_end = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    start = max(monday, not_before) if not_before else monday
    return start, sunday_end


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


def floor_to_slot(
    moment: datetime,
    open_time: time,
    close_time: time,
    interval_minutes: int,
) -> datetime:
    day_open = combine_date_time(moment.date(), open_time)
    day_close = combine_date_time(moment.date(), close_time)
    target = min(moment, day_close)
    if target <= day_open:
        return day_open
    step = timedelta(minutes=interval_minutes)
    steps = (target - day_open) // step
    return day_open + steps * step
