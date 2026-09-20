from datetime import datetime

from pydantic import BaseModel


class AvailableSlotsResponse(BaseModel):
    date: str
    is_open: bool
    total_duration_minutes: int
    slots: list[datetime]
