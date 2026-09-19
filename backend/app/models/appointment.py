from tortoise import fields

from .base import BaseModel
from app.enums import AppointmentStatus


class Appointment(BaseModel):
    customer: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="appointments",
        on_delete=fields.CASCADE,
    )
    scheduled_at = fields.DatetimeField(db_index=True)
    status = fields.CharEnumField(
        AppointmentStatus,
        default=AppointmentStatus.PENDING,
        max_length=20,
    )
    confirmed_at = fields.DatetimeField(null=True)
    notes = fields.TextField(null=True)

    services: fields.ReverseRelation["AppointmentService"]

    class Meta:
        table = "appointments"
