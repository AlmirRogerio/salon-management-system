from .repository import CustomerRepository, customer_repository
from .response import CustomerResponse


class CustomersService:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    async def list_customers(
        self, search: str | None = None
    ) -> list[CustomerResponse]:
        customers = await self._repository.list_customers(search)
        return [
            CustomerResponse(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                created_at=customer.created_at,
                appointments_count=getattr(customer, "appointments_count", 0)
                or 0,
                last_appointment_at=getattr(
                    customer, "last_appointment_at", None
                ),
            )
            for customer in customers
        ]


customers_service = CustomersService(customer_repository)
