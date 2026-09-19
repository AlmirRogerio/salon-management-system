from app.core.config import settings
from app.core.security import hash_password
from app.enums import UserRole
from app.models import User


async def seed_admin() -> None:
    email = settings.admin_email

    if await User.filter(email=email).exists():
        return

    await User.create(
        name=settings.admin_name,
        email=email,
        phone=settings.admin_phone,
        password_hash=hash_password(settings.admin_password),
        role=UserRole.ADMIN,
    )
