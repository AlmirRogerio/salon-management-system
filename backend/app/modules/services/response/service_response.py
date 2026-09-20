from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: Decimal
    duration_minutes: int
    active: bool
