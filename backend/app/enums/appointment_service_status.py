from enum import Enum


class AppointmentServiceStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"
