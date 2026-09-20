from datetime import time

from pydantic import BaseModel, Field, model_validator


class BusinessHoursDayDTO(BaseModel):
    weekday: int = Field(ge=0, le=6)
    is_open: bool = True
    open_time: time
    close_time: time
    slot_interval_minutes: int = Field(default=30, ge=1)

    @model_validator(mode="after")
    def _validate_range(self) -> "BusinessHoursDayDTO":
        if self.is_open and self.close_time <= self.open_time:
            raise ValueError(
                "O horario de fechamento deve ser maior que o de abertura."
            )
        return self


class UpdateBusinessHoursDTO(BaseModel):
    days: list[BusinessHoursDayDTO] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_unique_weekdays(self) -> "UpdateBusinessHoursDTO":
        weekdays = [day.weekday for day in self.days]
        if len(weekdays) != len(set(weekdays)):
            raise ValueError("Dias da semana duplicados na requisicao.")
        return self
