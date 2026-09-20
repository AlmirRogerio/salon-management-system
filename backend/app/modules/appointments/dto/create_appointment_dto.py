from datetime import datetime

from pydantic import BaseModel, Field


class CreateAppointmentDTO(BaseModel):
    scheduled_at: datetime
    service_ids: list[int] = Field(min_length=1)
    notes: str | None = Field(default=None, max_length=500)
