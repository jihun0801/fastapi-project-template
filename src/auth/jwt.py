from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt

from src import utils
from src.auth.config import auth_config
from src.auth.exceptions import (
    AuthorizationFailed,
    AuthRequired,
    ExpiredToken,
    InvalidToken,
)
from src.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=True)


def create_access_token(
    *,
    user: dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    jwt_data = {
        "sub": str(user["id"]),
        "exp": utils.get_kst_now() + expires_delta,
        "is_admin": user["is_admin"],
    }

    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )

    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_data(
    token: JWTData | None = Depends(parse_jwt_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_data),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()
