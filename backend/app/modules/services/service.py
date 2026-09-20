from fastapi import HTTPException, status

from .dto import CreateServiceDTO, UpdateServiceDTO
from .repository import ServiceRepository, service_repository
from .response import ServiceResponse


class ServiceService:
    def __init__(self, repository: ServiceRepository) -> None:
        self._repository = repository

    async def list_active(self) -> list[ServiceResponse]:
        services = await self._repository.list_active()
        return [ServiceResponse.model_validate(service) for service in services]

    async def list_all(self) -> list[ServiceResponse]:
        services = await self._repository.list_all()
        return [ServiceResponse.model_validate(service) for service in services]

    async def create(self, data: CreateServiceDTO) -> ServiceResponse:
        service = await self._repository.create(
            name=data.name,
            description=data.description,
            price=data.price,
            duration_minutes=data.duration_minutes,
            active=data.active,
        )
        return ServiceResponse.model_validate(service)

    async def update(
        self, service_id: int, data: UpdateServiceDTO
    ) -> ServiceResponse:
        service = await self._repository.get_by_id(service_id)
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servico nao encontrado.",
            )

        changes = data.model_dump(exclude_none=True)
        updated = await self._repository.update(service, changes)
        return ServiceResponse.model_validate(updated)


service_service = ServiceService(service_repository)
