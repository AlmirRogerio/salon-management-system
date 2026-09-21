from fastapi import APIRouter

from app.modules.appointments.controller import (
    admin_router as admin_appointments_router,
    router as appointments_router,
)
from app.modules.auth.controller import router as auth_router
from app.modules.business_hours.controller import router as business_hours_router
from app.modules.services.controller import router as services_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(services_router)
api_router.include_router(business_hours_router)
api_router.include_router(appointments_router)
api_router.include_router(admin_appointments_router)
