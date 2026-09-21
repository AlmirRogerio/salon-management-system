from datetime import date as date_cls, datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException, status

from app.enums import AppointmentServiceStatus, AppointmentStatus
from app.models import Appointment, Service
from app.modules.business_hours.repository import (
    BusinessHoursRepository,
    business_hours_repository,
)
from app.modules.services.repository import (
    ServiceRepository,
    service_repository,
)
from app.utils import (
    combine_date_time,
    now,
    overlaps_any,
    to_naive,
    week_bounds,
)

from .constants import ACTIVE_STATUSES, RESCHEDULE_MIN_DAYS
from .dto import (
    CreateAppointmentDTO,
    RescheduleAppointmentDTO,
    UpdateServiceStatusDTO,
)
from .repository import (
    AppointmentRepository,
    AppointmentServiceRepository,
    appointment_repository,
    appointment_service_repository,
)
from .response import (
    AdminAppointmentResponse,
    AppointmentResponse,
    AppointmentServiceResponse,
    AvailableSlotsResponse,
    WeekSuggestionResponse,
)


class AppointmentsService:
    def __init__(
        self,
        repository: AppointmentRepository,
        appointment_service_repo: AppointmentServiceRepository,
        services_repository: ServiceRepository,
        business_hours_repo: BusinessHoursRepository,
    ) -> None:
        self._repository = repository
        self._appointment_service_repository = appointment_service_repo
        self._services_repository = services_repository
        self._business_hours_repository = business_hours_repo

    async def create(
        self, customer_id: int, data: CreateAppointmentDTO
    ) -> AppointmentResponse:
        scheduled_at = to_naive(data.scheduled_at)
        self._ensure_future(
            scheduled_at, "A data do agendamento deve ser no futuro."
        )

        services = await self._get_valid_services(data.service_ids)
        total_duration = sum(s.duration_minutes for s in services)

        await self._ensure_within_business_hours(scheduled_at, total_duration)
        await self._ensure_no_conflict(scheduled_at, total_duration)

        appointment = await self._repository.create(
            customer_id=customer_id,
            scheduled_at=scheduled_at,
            notes=data.notes,
        )
        for service in services:
            await self._appointment_service_repository.create(
                appointment_id=appointment.id,
                service_id=service.id,
                price=service.price,
                duration_minutes=service.duration_minutes,
            )

        return await self.get_detail(appointment.id, customer_id)

    async def list_for_customer(
        self,
        customer_id: int,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[AppointmentResponse]:
        start = to_naive(start) if start else None
        end = to_naive(end) if end else None
        appointments = await self._repository.list_by_customer(
            customer_id, start=start, end=end
        )
        return [await self._build_response(item) for item in appointments]

    async def get_detail(
        self, appointment_id: int, customer_id: int
    ) -> AppointmentResponse:
        appointment = await self._get_or_404(appointment_id, customer_id)
        return await self._build_response(appointment)

    async def reschedule(
        self,
        appointment_id: int,
        customer_id: int,
        data: RescheduleAppointmentDTO,
    ) -> AppointmentResponse:
        appointment = await self._get_or_404(appointment_id, customer_id)

        self._ensure_not_final(appointment, "alterar")

        if not self._can_reschedule(appointment.scheduled_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "A alteracao pelo sistema so e permitida ate 2 dias antes. "
                    "Entre em contato com o salao por telefone."
                ),
            )

        new_date = to_naive(data.scheduled_at)
        self._ensure_future(
            new_date, "A nova data do agendamento deve ser no futuro."
        )

        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        total_duration = sum(item.duration_minutes for item in items)

        await self._ensure_within_business_hours(new_date, total_duration)
        await self._ensure_no_conflict(
            new_date, total_duration, exclude_id=appointment.id
        )

        appointment.scheduled_at = new_date
        await appointment.save()
        return await self._build_response(appointment)

    async def suggest_same_week(
        self, customer_id: int, target_date: datetime
    ) -> WeekSuggestionResponse:
        reference = to_naive(target_date)
        start, end = week_bounds(reference)
        existing = await self._repository.first_in_range(
            customer_id, start, end
        )
        if existing is None:
            return WeekSuggestionResponse(has_suggestion=False)
        return WeekSuggestionResponse(
            has_suggestion=True,
            suggested_date=to_naive(existing.scheduled_at),
            appointment_id=existing.id,
        )

    async def available_slots(
        self, target_date: date_cls, service_ids: list[int]
    ) -> AvailableSlotsResponse:
        services = await self._get_valid_services(service_ids)
        total_duration = sum(s.duration_minutes for s in services)

        hours = await self._business_hours_repository.get_by_weekday(
            target_date.weekday()
        )
        date_str = target_date.isoformat()

        if hours is None or not hours.is_open:
            return AvailableSlotsResponse(
                date=date_str,
                is_open=False,
                total_duration_minutes=total_duration,
                slots=[],
            )

        day_start = combine_date_time(target_date, hours.open_time)
        day_end = combine_date_time(target_date, hours.close_time)
        step = timedelta(minutes=hours.slot_interval_minutes)
        duration = timedelta(minutes=total_duration)

        occupied = await self._occupied_intervals(day_start, day_end)

        current = now()
        slots: list[datetime] = []
        cursor = day_start
        while cursor + duration <= day_end:
            slot_end = cursor + duration
            if cursor >= current and not overlaps_any(
                cursor, slot_end, occupied
            ):
                slots.append(cursor)
            cursor += step

        return AvailableSlotsResponse(
            date=date_str,
            is_open=True,
            total_duration_minutes=total_duration,
            slots=slots,
        )

    async def list_all(
        self,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
        statuses: list[str] | None = None,
    ) -> list[AdminAppointmentResponse]:
        start = to_naive(start) if start else None
        end = to_naive(end) if end else None
        appointments = await self._repository.list_all(
            start=start, end=end, statuses=statuses
        )
        return [
            await self._build_admin_response(item) for item in appointments
        ]

    async def get_admin_detail(
        self, appointment_id: int
    ) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)
        return await self._build_admin_response(appointment)

    async def confirm(self, appointment_id: int) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)

        if appointment.status != AppointmentStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somente agendamentos pendentes podem ser confirmados.",
            )

        appointment.status = AppointmentStatus.CONFIRMED
        appointment.confirmed_at = now()
        await appointment.save()
        return await self._build_admin_response(appointment)

    async def cancel(self, appointment_id: int) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)

        self._ensure_not_final(appointment, "cancelar")

        appointment.status = AppointmentStatus.CANCELED
        await appointment.save()

        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        for item in items:
            if item.status not in (
                AppointmentServiceStatus.COMPLETED,
                AppointmentServiceStatus.CANCELED,
            ):
                await self._appointment_service_repository.update_status(
                    item, AppointmentServiceStatus.CANCELED
                )

        return await self._build_admin_response(appointment)

    async def complete(self, appointment_id: int) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)

        self._ensure_not_final(appointment, "concluir")

        appointment.status = AppointmentStatus.COMPLETED
        await appointment.save()

        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        for item in items:
            if item.status not in (
                AppointmentServiceStatus.COMPLETED,
                AppointmentServiceStatus.CANCELED,
            ):
                await self._appointment_service_repository.update_status(
                    item, AppointmentServiceStatus.COMPLETED
                )

        return await self._build_admin_response(appointment)

    async def admin_reschedule(
        self, appointment_id: int, data: RescheduleAppointmentDTO
    ) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)

        self._ensure_not_final(appointment, "alterar")

        new_date = to_naive(data.scheduled_at)
        self._ensure_future(
            new_date, "A nova data do agendamento deve ser no futuro."
        )

        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        total_duration = sum(item.duration_minutes for item in items)

        await self._ensure_within_business_hours(new_date, total_duration)
        await self._ensure_no_conflict(
            new_date, total_duration, exclude_id=appointment.id
        )

        appointment.scheduled_at = new_date
        await appointment.save()
        return await self._build_admin_response(appointment)

    async def update_service_status(
        self,
        appointment_id: int,
        service_row_id: int,
        data: UpdateServiceStatusDTO,
    ) -> AdminAppointmentResponse:
        appointment = await self._get_or_404(appointment_id)

        item = await self._appointment_service_repository.get_for_appointment(
            appointment_id, service_row_id
        )
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servico do agendamento nao encontrado.",
            )

        await self._appointment_service_repository.update_status(
            item, data.status
        )

        return await self._build_admin_response(appointment)

    async def _get_or_404(
        self, appointment_id: int, customer_id: int | None = None
    ) -> Appointment:
        appointment = await (
            self._repository.get_with_customer(appointment_id)
            if customer_id is None
            else self._repository.get_owned(appointment_id, customer_id)
        )
        if appointment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento nao encontrado.",
            )
        return appointment

    def _is_final(self, appointment_status: AppointmentStatus) -> bool:
        return appointment_status in (
            AppointmentStatus.COMPLETED,
            AppointmentStatus.CANCELED,
        )

    def _ensure_not_final(
        self, appointment: Appointment, action: str
    ) -> None:
        if self._is_final(appointment.status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Nao e possivel {action} um agendamento finalizado ou cancelado."
                ),
            )

    def _ensure_future(self, moment: datetime, detail: str) -> None:
        if moment <= now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )

    async def _build_admin_response(
        self, appointment: Appointment
    ) -> AdminAppointmentResponse:
        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        service_responses = [
            AppointmentServiceResponse(
                id=item.id,
                service_id=item.service_id,
                service_name=item.service.name,
                status=item.status,
                price=item.price,
                duration_minutes=item.duration_minutes,
            )
            for item in items
        ]
        total_price = sum(
            (item.price for item in items), start=Decimal("0")
        )
        total_duration = sum(item.duration_minutes for item in items)

        customer = appointment.customer

        return AdminAppointmentResponse(
            id=appointment.id,
            customer_id=appointment.customer_id,
            customer_name=customer.name,
            customer_phone=customer.phone,
            scheduled_at=to_naive(appointment.scheduled_at),
            status=appointment.status,
            confirmed_at=(
                to_naive(appointment.confirmed_at)
                if appointment.confirmed_at
                else None
            ),
            notes=appointment.notes,
            total_price=total_price,
            total_duration_minutes=total_duration,
            services=service_responses,
        )

    async def _occupied_intervals(
        self,
        day_start: datetime,
        day_end: datetime,
        *,
        exclude_id: int | None = None,
    ) -> list[tuple[datetime, datetime]]:
        appointments = await self._repository.list_active_in_range(
            day_start, day_end, ACTIVE_STATUSES, exclude_id=exclude_id
        )
        if not appointments:
            return []

        appointment_ids = [appt.id for appt in appointments]
        items = await self._appointment_service_repository.list_by_appointment_ids(
            appointment_ids
        )
        duration_by_appointment: dict[int, int] = {}
        for item in items:
            duration_by_appointment[item.appointment_id] = (
                duration_by_appointment.get(item.appointment_id, 0)
                + item.duration_minutes
            )

        intervals: list[tuple[datetime, datetime]] = []
        for appt in appointments:
            minutes = duration_by_appointment.get(appt.id, 0)
            start = to_naive(appt.scheduled_at)
            intervals.append((start, start + timedelta(minutes=minutes)))
        return intervals

    def _can_reschedule(self, scheduled_at: datetime) -> bool:
        return to_naive(scheduled_at) - now() >= timedelta(
            days=RESCHEDULE_MIN_DAYS
        )

    async def _get_valid_services(
        self, service_ids: list[int]
    ) -> list[Service]:
        unique_ids = list(dict.fromkeys(service_ids))
        services = await self._services_repository.get_active_by_ids(
            unique_ids
        )
        if len(services) != len(unique_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um ou mais servicos sao invalidos ou estao inativos.",
            )
        return services

    async def _ensure_within_business_hours(
        self, start: datetime, total_duration_minutes: int
    ) -> None:
        hours = await self._business_hours_repository.get_by_weekday(
            start.weekday()
        )
        if hours is None or not hours.is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O salao esta fechado nesse dia.",
            )

        day = start.date()
        open_at = combine_date_time(day, hours.open_time)
        close_at = combine_date_time(day, hours.close_time)
        end = start + timedelta(minutes=total_duration_minutes)

        if start < open_at or end > close_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O horario esta fora do expediente do salao.",
            )

    async def _ensure_no_conflict(
        self,
        start: datetime,
        total_duration_minutes: int,
        *,
        exclude_id: int | None = None,
    ) -> None:
        end = start + timedelta(minutes=total_duration_minutes)
        day_start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        occupied = await self._occupied_intervals(
            day_start, day_end, exclude_id=exclude_id
        )
        if overlaps_any(start, end, occupied):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ja existe um agendamento nesse horario.",
            )

    async def _build_response(
        self, appointment: Appointment
    ) -> AppointmentResponse:
        items = await self._appointment_service_repository.list_by_appointment(
            appointment.id
        )
        service_responses = [
            AppointmentServiceResponse(
                id=item.id,
                service_id=item.service_id,
                service_name=item.service.name,
                status=item.status,
                price=item.price,
                duration_minutes=item.duration_minutes,
            )
            for item in items
        ]
        total_price = sum(
            (item.price for item in items), start=Decimal("0")
        )
        total_duration = sum(item.duration_minutes for item in items)

        return AppointmentResponse(
            id=appointment.id,
            scheduled_at=to_naive(appointment.scheduled_at),
            status=appointment.status,
            confirmed_at=(
                to_naive(appointment.confirmed_at)
                if appointment.confirmed_at
                else None
            ),
            notes=appointment.notes,
            total_price=total_price,
            total_duration_minutes=total_duration,
            can_reschedule=(
                not self._is_final(appointment.status)
                and self._can_reschedule(appointment.scheduled_at)
            ),
            services=service_responses,
        )


appointments_service = AppointmentsService(
    appointment_repository,
    appointment_service_repository,
    service_repository,
    business_hours_repository,
)
