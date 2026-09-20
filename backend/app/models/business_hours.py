from tortoise import fields
from tortoise.validators import MaxValueValidator, MinValueValidator

from .base import BaseModel


class BusinessHours(BaseModel):
    weekday = fields.SmallIntField(
        unique=True,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
    )
    is_open = fields.BooleanField(default=True)
    open_time = fields.TimeField()
    close_time = fields.TimeField()
    slot_interval_minutes = fields.IntField(
        default=30,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        table = "business_hours"
