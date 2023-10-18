import uuid
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4
from sqlalchemy import insert, select, update


from src import utils
from src.auth.config import auth_config
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import Login, UserCreate
from src.auth.security import hash_password, check_password
from src.database import auth_refresh_token, auth_user, execute, fetch_one


async def create_user(create_user_data: UserCreate) -> dict[str, Any] | None:
    values = create_user_data.serializable_dict(exclude_defaults=True)
    values["login_password"] = hash_password(values["login_password"])
    insert_query = (
        insert(auth_user)
        .values(values)
        .returning(auth_user)
    )

    return await fetch_one(insert_query)


async def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.id == user_id)

    return await fetch_one(select_query)


async def get_user_by_nick_name(nick_name: str) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.nick_name == nick_name)

    return await fetch_one(select_query)


async def get_user_by_login_id(login_id: str) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.login_id == login_id)

    return await fetch_one(select_query)


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = insert(auth_refresh_token).values(
        uuid=uuid.uuid4(),
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await execute(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    select_query = select(auth_refresh_token).where(
        auth_refresh_token.c.refresh_token == refresh_token
    )

    return await fetch_one(select_query)


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    update_query = (
        update(auth_refresh_token)
        .values(expires_at=utils.get_kst_now() - timedelta(days=1))
        .where(auth_refresh_token.c.uuid == refresh_token_uuid)
    )

    await execute(update_query)


async def login(login_data: Login) -> dict[str, Any]:
    user = await get_user_by_login_id(login_data.login_id)
    if not user:
        raise InvalidCredentials()

    if not check_password(login_data.login_password, user["login_password"]):
        raise InvalidCredentials()

    return user
