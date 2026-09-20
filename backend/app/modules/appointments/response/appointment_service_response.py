from decimal import Decimal

from pydantic import BaseModel

from app.enums import AppointmentServiceStatus


class AppointmentServiceResponse(BaseModel):
    id: int
    service_id: int
    service_name: str
    status: AppointmentServiceStatus
    price: Decimal
    duration_minutes: int
