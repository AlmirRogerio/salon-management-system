from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    created_at: datetime
