from datetime import date, datetime

from fastapi import APIRouter, Depends, Query, status

from app.models import User
from app.modules.auth.dependencies import get_current_user

from .dto import CreateAppointmentDTO, RescheduleAppointmentDTO
from .response import (
    AppointmentResponse,
    AvailableSlotsResponse,
    WeekSuggestionResponse,
)
from .service import appointments_service

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    data: CreateAppointmentDTO,
    current_user: User = Depends(get_current_user),
) -> AppointmentResponse:
    return await appointments_service.create(current_user.id, data)


@router.get("", response_model=list[AppointmentResponse])
async def list_appointments(
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    current_user: User = Depends(get_current_user),
) -> list[AppointmentResponse]:
    return await appointments_service.list_for_customer(current_user.id, start=start, end=end)


@router.get("/week-suggestion", response_model=WeekSuggestionResponse)
async def week_suggestion(
    target_date: datetime = Query(...),
    current_user: User = Depends(get_current_user),
) -> WeekSuggestionResponse:
    return await appointments_service.suggest_same_week(current_user.id, target_date)


@router.get("/available-slots", response_model=AvailableSlotsResponse)
async def available_slots(
    date: date = Query(...),
    service_ids: list[int] = Query(...),
    _current_user: User = Depends(get_current_user),
) -> AvailableSlotsResponse:
    return await appointments_service.available_slots(date, service_ids)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
) -> AppointmentResponse:
    return await appointments_service.get_detail(appointment_id, current_user.id)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def reschedule_appointment(
    appointment_id: int,
    data: RescheduleAppointmentDTO,
    current_user: User = Depends(get_current_user),
) -> AppointmentResponse:
    return await appointments_service.reschedule(appointment_id, current_user.id, data)
