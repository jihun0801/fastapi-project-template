import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from src.constants import RouterPrefix
from src.auth.constants import Path, ErrorMessage


prefix_path = RouterPrefix.MAIN + RouterPrefix.AUTH


@pytest.mark.asyncio
async def test_create_user(client: TestClient) -> None:
    request_body = {
        "login_id": "test_id",
        "login_password": "a123!@",
        "user_name": "park",
        "nick_name": "park",
    }
    response = await client.post(
        prefix_path + Path.CREATE_USER,
        json=request_body
    )
    response_body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response_body
    assert response_body["login_id"] == request_body["login_id"]
    assert response_body["user_name"] == request_body["user_name"]
    assert response_body["nick_name"] == request_body["nick_name"]


@pytest.mark.asyncio
async def test_create_user_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.auth.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_login_id", fake_getter)
    request_body = {
        "login_id": "test_id",
        "login_password": "a123!@",
        "user_name": "park",
        "nick_name": "park",
    }
    response = await client.post(
        prefix_path + Path.CREATE_USER,
        json=request_body
    )
    response_body = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_body["detail"] == ErrorMessage.LOGIN_ID_TAKEN


@pytest.mark.asyncio
async def test_login(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    request_body = {
        "login_id": "test_id",
        "login_password": "a123!@",
    }
    response = await client.post(
        prefix_path + Path.LOGIN,
        json=request_body
    )
    response_body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_body
    assert "refresh_token" in response_body


@pytest.mark.asyncio
async def test_get_me(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    login_request_body = {
        "login_id": "test_id",
        "login_password": "a123!@",
    }
    login_response = await client.post(
        prefix_path + Path.LOGIN,
        json=login_request_body
    )
    login_response_body = login_response.json()

    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response_body
    assert "refresh_token" in login_response_body

    access_token = login_response_body["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    read_user_response = await client.get(
        prefix_path + Path.READ_USER_ME,
        headers=headers
    )
    read_user_response_body = read_user_response.json()

    assert read_user_response.status_code == status.HTTP_200_OK
    assert "id" in read_user_response_body
