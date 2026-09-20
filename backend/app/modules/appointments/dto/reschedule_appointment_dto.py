from datetime import datetime

from pydantic import BaseModel


class RescheduleAppointmentDTO(BaseModel):
    scheduled_at: datetime
