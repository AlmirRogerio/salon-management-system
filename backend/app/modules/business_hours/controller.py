from fastapi import APIRouter, Depends

from app.models import User
from app.modules.auth.dependencies import get_current_admin

from .dto import UpdateBusinessHoursDTO
from .response import BusinessHoursResponse
from .service import business_hours_service

router = APIRouter(prefix="/business-hours", tags=["business-hours"])


@router.get("", response_model=list[BusinessHoursResponse])
async def list_business_hours(
    _admin: User = Depends(get_current_admin),
) -> list[BusinessHoursResponse]:
    return await business_hours_service.list_all()


@router.put("", response_model=list[BusinessHoursResponse])
async def update_business_hours(
    data: UpdateBusinessHoursDTO,
    _admin: User = Depends(get_current_admin),
) -> list[BusinessHoursResponse]:
    return await business_hours_service.update(data)
