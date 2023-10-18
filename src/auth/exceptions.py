from src.auth.constants import ErrorMessage
from src.exceptions import (
    BadRequest,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
)


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorMessage.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorMessage.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_TOKEN


class ExpiredToken(NotAuthenticated):
    DETAIL = ErrorMessage.EXPIRED_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorMessage.INVALID_CREDENTIALS


class LoginIdTaken(BadRequest):
    DETAIL = ErrorMessage.LOGIN_ID_TAKEN


class NickNameTaken(BadRequest):
    DETAIL = ErrorMessage.NICK_NAME_TAKEN


class InvalidPasswordPattern(BadRequest):
    DETAIL = ErrorMessage.INVALID_PASSWORD_PATTERN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorMessage.REFRESH_TOKEN_NOT_VALID


class UserNotFound(NotFound):
    DETAIL = ErrorMessage.USER_NOT_FOUND
