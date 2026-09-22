from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    created_at: datetime
    appointments_count: int
    last_appointment_at: datetime | None
