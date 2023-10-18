class Path:
    CREATE_USER = "/user"
    READ_USER = "/user/{nick_name}"
    READ_USER_ME = "/user/me"
    LOGIN = "/login"
    LOGOUT = "/logout"
    TOKEN_UPDATE = "/token"


class ErrorMessage:
    AUTHENTICATION_REQUIRED = "로그인이 필요합니다."
    AUTHORIZATION_FAILED = "권한이 없습니다."
    INVALID_TOKEN = "유효 하지 않은 토큰 입니다."
    EXPIRED_TOKEN = "만료된 토큰입니다."
    INVALID_CREDENTIALS = "아이디 또는 비밀 번호를 확인해 주세요."
    LOGIN_ID_TAKEN = "이미 존재 하는 계정 입니다."
    NICK_NAME_TAKEN = "이미 존재 하는 닉네임 입니다."
    INVALID_PASSWORD_PATTERN = (
        "비밀 번호는 다음과 같은 조건을 만족 해야 합니다. \n"
        "최소6자 최소32자 "
        "최소 하나 이상의 숫자 "
        "최소 하나 이상의 특수 문자 "
    )
    USER_NOT_FOUND = "해당 유저를 찾을 수 없습니다."
    REFRESH_TOKEN_NOT_VALID = "유효 하지 않은 refresh token 입니다."
    REFRESH_TOKEN_REQUIRED = "refresh token이 존재 하지 않습니다."
