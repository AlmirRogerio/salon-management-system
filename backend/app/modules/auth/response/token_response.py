from pydantic import BaseModel

from .user_response import UserResponse


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenWithUserResponse(TokenResponse):
    user: UserResponse
