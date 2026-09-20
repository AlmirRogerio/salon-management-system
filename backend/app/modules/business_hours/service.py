from .dto import UpdateBusinessHoursDTO
from .repository import (
    BusinessHoursRepository,
    business_hours_repository,
)
from .response import BusinessHoursResponse


class BusinessHoursService:
    def __init__(self, repository: BusinessHoursRepository) -> None:
        self._repository = repository

    async def list_all(self) -> list[BusinessHoursResponse]:
        records = await self._repository.list_all()
        return [BusinessHoursResponse.model_validate(r) for r in records]

    async def update(
        self, data: UpdateBusinessHoursDTO
    ) -> list[BusinessHoursResponse]:
        for day in data.days:
            await self._repository.upsert(
                weekday=day.weekday,
                is_open=day.is_open,
                open_time=day.open_time,
                close_time=day.close_time,
                slot_interval_minutes=day.slot_interval_minutes,
            )
        return await self.list_all()


business_hours_service = BusinessHoursService(business_hours_repository)
