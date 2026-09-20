from fastapi import APIRouter

from app.modules.auth.controller import router as auth_router
from app.modules.business_hours.controller import router as business_hours_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(business_hours_router)
