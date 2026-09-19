from tortoise import fields

from .base import BaseModel
from app.enums import UserRole


class User(BaseModel):
    name = fields.CharField(max_length=150)
    email = fields.CharField(max_length=255, unique=True, db_index=True)
    phone = fields.CharField(max_length=30)
    password_hash = fields.CharField(max_length=255)
    role = fields.CharEnumField(
        UserRole,
        default=UserRole.CUSTOMER,
        max_length=20,
    )

    appointments: fields.ReverseRelation["Appointment"]

    class Meta:
        table = "users"
