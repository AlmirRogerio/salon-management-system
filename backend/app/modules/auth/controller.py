from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import User

from .dependencies import get_current_user
from .dto import LoginDTO, RegisterDTO
from .response import TokenResponse, TokenWithUserResponse, UserResponse
from .service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenWithUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(data: RegisterDTO) -> TokenWithUserResponse:
    return await auth_service.register(data)


@router.post("/login", response_model=TokenWithUserResponse)
async def login(data: LoginDTO) -> TokenWithUserResponse:
    return await auth_service.login(data)


@router.post("/token", response_model=TokenResponse)
async def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    return await auth_service.issue_token(
        LoginDTO(email=form_data.username, password=form_data.password)
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
