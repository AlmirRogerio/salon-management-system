from datetime import datetime

from pydantic import BaseModel


class WeekSuggestionResponse(BaseModel):
    has_suggestion: bool
    suggested_date: datetime | None = None
    appointment_id: int | None = None
