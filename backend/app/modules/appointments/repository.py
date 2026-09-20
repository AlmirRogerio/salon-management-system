from datetime import datetime

from app.models import Appointment, AppointmentService


class AppointmentRepository:
    async def create(
        self,
        *,
        customer_id: int,
        scheduled_at: datetime,
        notes: str | None,
    ) -> Appointment:
        return await Appointment.create(
            customer_id=customer_id,
            scheduled_at=scheduled_at,
            notes=notes,
        )

    async def get_owned(
        self, appointment_id: int, customer_id: int
    ) -> Appointment | None:
        return await Appointment.filter(
            id=appointment_id, customer_id=customer_id
        ).first()

    async def list_by_customer(
        self,
        customer_id: int,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[Appointment]:
        query = Appointment.filter(customer_id=customer_id)
        if start is not None:
            query = query.filter(scheduled_at__gte=start)
        if end is not None:
            query = query.filter(scheduled_at__lte=end)
        return await query.order_by("-scheduled_at")

    async def first_in_range(
        self,
        customer_id: int,
        start: datetime,
        end: datetime,
        *,
        exclude_id: int | None = None,
    ) -> Appointment | None:
        query = Appointment.filter(
            customer_id=customer_id,
            scheduled_at__gte=start,
            scheduled_at__lte=end,
        )
        if exclude_id is not None:
            query = query.exclude(id=exclude_id)
        return await query.order_by("scheduled_at").first()

    async def list_active_in_range(
        self,
        start: datetime,
        end: datetime,
        statuses: list[str],
        *,
        exclude_id: int | None = None,
    ) -> list[Appointment]:
        query = Appointment.filter(
            scheduled_at__gte=start,
            scheduled_at__lt=end,
            status__in=statuses,
        )
        if exclude_id is not None:
            query = query.exclude(id=exclude_id)
        return await query.order_by("scheduled_at")


appointment_repository = AppointmentRepository()


class AppointmentServiceRepository:
    async def create(
        self,
        *,
        appointment_id: int,
        service_id: int,
        price,
        duration_minutes: int,
    ) -> AppointmentService:
        return await AppointmentService.create(
            appointment_id=appointment_id,
            service_id=service_id,
            price=price,
            duration_minutes=duration_minutes,
        )

    async def list_by_appointment(
        self, appointment_id: int
    ) -> list[AppointmentService]:
        return (
            await AppointmentService.filter(appointment_id=appointment_id)
            .select_related("service")
            .order_by("id")
        )

    async def list_by_appointment_ids(
        self, appointment_ids: list[int]
    ) -> list[AppointmentService]:
        return await AppointmentService.filter(
            appointment_id__in=appointment_ids
        )


appointment_service_repository = AppointmentServiceRepository()
