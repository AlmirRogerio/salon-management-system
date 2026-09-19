from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models import User

from .dto import LoginDTO, RegisterDTO
from .repository import UserRepository, user_repository
from .response import TokenResponse, TokenWithUserResponse, UserResponse


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register(self, data: RegisterDTO) -> TokenWithUserResponse:
        if await self._repository.exists_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail ja cadastrado.",
            )

        user = await self._repository.create(
            name=data.name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(data.password),
        )
        return self._build_token_with_user(user)

    async def login(self, data: LoginDTO) -> TokenWithUserResponse:
        user = await self._authenticate(data)
        return self._build_token_with_user(user)

    async def issue_token(self, data: LoginDTO) -> TokenResponse:
        user = await self._authenticate(data)
        return self._build_token(user)

    async def _authenticate(self, data: LoginDTO) -> User:
        user = await self._repository.get_by_email(data.email)
        if user is None or not verify_password(
            data.password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais invalidas.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def _build_token(self, user: User) -> TokenResponse:
        return TokenResponse(access_token=create_access_token(subject=user.id))

    def _build_token_with_user(self, user: User) -> TokenWithUserResponse:
        token = self._build_token(user)
        return TokenWithUserResponse(
            access_token=token.access_token,
            token_type=token.token_type,
            user=UserResponse.model_validate(user),
        )


auth_service = AuthService(user_repository)
