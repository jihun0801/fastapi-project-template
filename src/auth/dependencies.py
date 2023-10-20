import re
from datetime import datetime
from typing import Any

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth import utils as auth_utils
from src.auth.exceptions import (
    InvalidPasswordPattern,
    LoginIdTaken,
    NickNameTaken,
    RefreshTokenNotValid,
    UserNotFound,
)
from src.auth.schemas import UserCreate
from src.database.core import get_db_session


async def valid_user_create(
    create_user_data: UserCreate, db_session: AsyncSession = Depends(get_db_session)
) -> UserCreate:
    if await service.get_user_by_login_id(
        db_session=db_session, login_id=create_user_data.login_id
    ):
        raise LoginIdTaken()

    if await service.get_user_by_nick_name(
        db_session=db_session, nick_name=create_user_data.nick_name
    ):
        raise NickNameTaken()

    if not re.match(
        pattern=auth_utils.STRONG_PASSWORD_PATTERN,
        string=create_user_data.login_password,
    ):
        raise InvalidPasswordPattern()

    return create_user_data


async def valid_user_nick_name(
    user_nick_name: str, db_session: AsyncSession = Depends(get_db_session)
) -> str:
    if not await service.get_user_by_nick_name(
        db_session=db_session, nick_name=user_nick_name
    ):
        raise UserNotFound()

    return user_nick_name


async def valid_refresh_token(
    db_session: AsyncSession = Depends(get_db_session),
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await service.get_refresh_token(
        db_session=db_session, refresh_token=refresh_token
    )
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token=db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    db_session: AsyncSession = Depends(get_db_session),
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await service.get_user_by_id(
        db_session=db_session, user_id=refresh_token["user_id"]
    )
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
