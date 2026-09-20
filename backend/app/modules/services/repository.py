from decimal import Decimal

from app.models import Service


class ServiceRepository:
    async def list_active(self) -> list[Service]:
        return await Service.filter(active=True).order_by("name")

    async def list_all(self) -> list[Service]:
        return await Service.all().order_by("name")

    async def get_active_by_ids(self, ids: list[int]) -> list[Service]:
        return await Service.filter(id__in=ids, active=True)

    async def get_by_id(self, service_id: int) -> Service | None:
        return await Service.filter(id=service_id).first()

    async def create(
        self,
        *,
        name: str,
        description: str,
        price: Decimal,
        duration_minutes: int,
        active: bool,
    ) -> Service:
        return await Service.create(
            name=name,
            description=description,
            price=price,
            duration_minutes=duration_minutes,
            active=active,
        )

    async def update(self, service: Service, changes: dict) -> Service:
        for field, value in changes.items():
            setattr(service, field, value)
        await service.save()
        return service


service_repository = ServiceRepository()
