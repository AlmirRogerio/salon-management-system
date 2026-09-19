from app.models import User


class UserRepository:
    async def get_by_email(self, email: str) -> User | None:
        return await User.filter(email=email).first()

    async def get_by_id(self, user_id: int) -> User | None:
        return await User.get_or_none(id=user_id)

    async def exists_by_email(self, email: str) -> bool:
        return await User.filter(email=email).exists()

    async def create(
        self,
        *,
        name: str,
        email: str,
        phone: str,
        password_hash: str,
    ) -> User:
        return await User.create(
            name=name,
            email=email,
            phone=phone,
            password_hash=password_hash,
        )


user_repository = UserRepository()
