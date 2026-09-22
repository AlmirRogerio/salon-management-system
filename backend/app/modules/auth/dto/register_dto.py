import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterDTO(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) < 10 or len(digits) > 11:
            raise ValueError(
                "Telefone invalido. Informe DDD e numero, ex: (11) 99999-9999."
            )
        return digits
