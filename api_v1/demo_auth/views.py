import secrets
import uuid
from time import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix="/demo-auth", tags=["demo-auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hello!",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "john": "eggs",
}


static_auth_token_to_username = {
    "f89e14d25f30b24a70ad4c0cb745": "admin",
    "e12c3dd98209eeed32f5eeb47151145fe160": "eggs",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if token := static_auth_token_to_username.get(static_token):
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )


@router.get("/basic-auth-username/")
def demo_basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        "message": f"Hello, {auth_username}!",
        "username": auth_username,
    }


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hello, {username}!",
        "username": username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return COOKIES[session_id]


@router.post("/login-cookie/")
def demo_auth_login_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_user_username),
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        "result": "ok",
    }


@router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}!",
        **user_session_data,
    }


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
        **user_session_data,
    }
