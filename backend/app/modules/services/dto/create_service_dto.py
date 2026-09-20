from decimal import Decimal

from pydantic import BaseModel, Field


class CreateServiceDTO(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    duration_minutes: int = Field(ge=1)
    active: bool = True
