from app.enums import AppointmentStatus

RESCHEDULE_MIN_DAYS = 2

ACTIVE_STATUSES = [
    AppointmentStatus.PENDING.value,
    AppointmentStatus.CONFIRMED.value,
    AppointmentStatus.COMPLETED.value,
]
