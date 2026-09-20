from datetime import time, timedelta

from pydantic import BaseModel, ConfigDict, field_validator


class BusinessHoursResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    weekday: int
    is_open: bool
    open_time: time
    close_time: time
    slot_interval_minutes: int

    @field_validator("open_time", "close_time", mode="before")
    @classmethod
    def _coerce_time(cls, value: object) -> object:
        if isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return time(hour=hours, minute=minutes, second=seconds)
        return value
