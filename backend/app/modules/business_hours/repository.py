from app.models import BusinessHours


class BusinessHoursRepository:
    async def list_all(self) -> list[BusinessHours]:
        return await BusinessHours.all().order_by("weekday")

    async def get_by_weekday(self, weekday: int) -> BusinessHours | None:
        return await BusinessHours.filter(weekday=weekday).first()

    async def upsert(
        self,
        *,
        weekday: int,
        is_open: bool,
        open_time,
        close_time,
        slot_interval_minutes: int,
    ) -> BusinessHours:
        defaults = {
            "is_open": is_open,
            "open_time": open_time,
            "close_time": close_time,
            "slot_interval_minutes": slot_interval_minutes,
        }
        record, created = await BusinessHours.get_or_create(
            weekday=weekday, defaults=defaults
        )
        if not created:
            record.is_open = is_open
            record.open_time = open_time
            record.close_time = close_time
            record.slot_interval_minutes = slot_interval_minutes
            await record.save()

        return record


business_hours_repository = BusinessHoursRepository()
