from tortoise.expressions import Q
from tortoise.functions import Count, Max

from app.enums import UserRole
from app.models import User


class CustomerRepository:
    async def list_customers(self, search: str | None = None) -> list[User]:
        query = User.filter(role=UserRole.CUSTOMER)
        if search:
            term = search.strip()
            if term:
                query = query.filter(
                    Q(name__icontains=term)
                    | Q(email__icontains=term)
                    | Q(phone__icontains=term)
                )
        query = query.annotate(
            appointments_count=Count("appointments__id"),
            last_appointment_at=Max("appointments__scheduled_at"),
        )
        return await query.order_by("name")


customer_repository = CustomerRepository()
