from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class UpdateServiceDTO(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(
        default=None, ge=0, max_digits=10, decimal_places=2
    )
    duration_minutes: int | None = Field(default=None, ge=1)
    active: bool | None = None

    @model_validator(mode="after")
    def _validate_any_field(self) -> "UpdateServiceDTO":
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar.")
        return self
