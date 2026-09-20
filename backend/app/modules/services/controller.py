from fastapi import APIRouter, Depends, status

from app.models import User
from app.modules.auth.dependencies import get_current_admin, get_current_user

from .dto import CreateServiceDTO, UpdateServiceDTO
from .response import ServiceResponse
from .service import service_service

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceResponse])
async def list_services(
    _current_user: User = Depends(get_current_user),
) -> list[ServiceResponse]:
    return await service_service.list_active()


@router.get("/all", response_model=list[ServiceResponse])
async def list_all_services(
    _admin: User = Depends(get_current_admin),
) -> list[ServiceResponse]:
    return await service_service.list_all()


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    data: CreateServiceDTO,
    _admin: User = Depends(get_current_admin),
) -> ServiceResponse:
    return await service_service.create(data)


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    data: UpdateServiceDTO,
    _admin: User = Depends(get_current_admin),
) -> ServiceResponse:
    return await service_service.update(service_id, data)
