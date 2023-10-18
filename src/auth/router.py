from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.auth import jwt, service, utils
from src.auth.constants import Path
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
    valid_user_nick_name,
)
from src.auth.jwt import parse_jwt_data
from src.auth.schemas import (
    AccessTokenResponse,
    JWTData,
    Login,
    User,
    UserCreate,
    UserDetail,
)

router = APIRouter()


@router.post(
    Path.CREATE_USER,
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetail,
    description="새로운 유저를 생성한다.",
)
async def create_user(
    create_user_data: UserCreate = Depends(valid_user_create),
) -> UserDetail:
    return await service.create_user(create_user_data)


@router.get(
    Path.READ_USER_ME,
    status_code=status.HTTP_200_OK,
    response_model=UserDetail,
    description="내 정보를 확인한다.",
)
async def get_me(jwt_data: JWTData = Depends(parse_jwt_data)) -> UserDetail:
    return await service.get_user_by_id(jwt_data.user_id)


@router.get(
    Path.READ_USER,
    status_code=status.HTTP_200_OK,
    response_model=User,
    description="유저 정보를 확인한다.",
)
async def get_user(user_nick_name: str = Depends(valid_user_nick_name)) -> User:
    return await service.get_user_by_nick_name(user_nick_name)


@router.post(
    Path.LOGIN,
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenResponse,
    description="로그인을 수행하고 토큰을 발급받는다.",
)
async def login(login_data: Login, response: Response) -> AccessTokenResponse:
    user = await service.login(login_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put(
    Path.TOKEN_UPDATE,
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenResponse,
    description="기존 refresh token으로 refresh token과 access token을 재발급 받는다.",
)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete(
    Path.LOGOUT, status_code=status.HTTP_200_OK, description="토큰을 만료하여 로그아웃을 수행한다."
)
async def logout(
    response: Response, refresh_token: dict[str, Any] = Depends(valid_refresh_token)
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
