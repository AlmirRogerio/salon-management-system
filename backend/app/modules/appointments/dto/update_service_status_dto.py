from pydantic import BaseModel

from app.enums import AppointmentServiceStatus


class UpdateServiceStatusDTO(BaseModel):
    status: AppointmentServiceStatus
