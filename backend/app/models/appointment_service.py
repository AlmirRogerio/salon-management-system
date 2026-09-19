from tortoise import fields
from tortoise.validators import MinValueValidator

from .base import BaseModel
from app.enums import AppointmentServiceStatus


class AppointmentService(BaseModel):
    appointment: fields.ForeignKeyRelation["Appointment"] = fields.ForeignKeyField(
        "models.Appointment",
        related_name="services",
        on_delete=fields.CASCADE,
    )
    service: fields.ForeignKeyRelation["Service"] = fields.ForeignKeyField(
        "models.Service",
        related_name="appointment_services",
        on_delete=fields.RESTRICT,
    )
    status = fields.CharEnumField(
        AppointmentServiceStatus,
        default=AppointmentServiceStatus.PENDING,
        max_length=20,
    )
    price = fields.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    duration_minutes = fields.IntField(validators=[MinValueValidator(1)])

    class Meta:
        table = "appointment_services"
        unique_together = (("appointment", "service"),)
