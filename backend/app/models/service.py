from tortoise import fields
from tortoise.validators import MinValueValidator

from .base import BaseModel


class Service(BaseModel):
    name = fields.CharField(max_length=150)
    description = fields.TextField()
    price = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    duration_minutes = fields.IntField(validators=[MinValueValidator(1)])
    active = fields.BooleanField(default=True)

    appointment_services: fields.ReverseRelation["AppointmentService"]

    class Meta:
        table = "services"
