from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, Field

from src.models import CustomModel


class User(CustomModel):
    user_name: str
    nick_name: str
    image_url: str | None


class UserDetail(User):
    id: int
    login_id: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None


class UserCreate(CustomModel):
    login_id: str
    login_password: str
    user_name: str
    nick_name: str
    image_url: Optional[AnyUrl] = None


class Login(CustomModel):
    login_id: str
    login_password: str = Field(min_length=6, max_length=32)


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str
