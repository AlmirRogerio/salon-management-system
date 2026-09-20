from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.enums import AppointmentStatus

from .appointment_service_response import AppointmentServiceResponse


class AppointmentResponse(BaseModel):
    id: int
    scheduled_at: datetime
    status: AppointmentStatus
    confirmed_at: datetime | None
    notes: str | None
    total_price: Decimal
    total_duration_minutes: int
    can_reschedule: bool
    services: list[AppointmentServiceResponse]
