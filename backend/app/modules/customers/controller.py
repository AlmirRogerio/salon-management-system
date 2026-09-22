from fastapi import APIRouter, Depends, Query

from app.models import User
from app.modules.auth.dependencies import get_current_admin

from .response import CustomerResponse
from .service import customers_service

router = APIRouter(prefix="/admin/customers", tags=["admin-customers"])


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    search: str | None = Query(default=None),
    _admin: User = Depends(get_current_admin),
) -> list[CustomerResponse]:
    return await customers_service.list_customers(search)
