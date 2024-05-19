from typing import NoReturn
import warnings
from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from backend import BackendService, NotAuthorizedError
from dependencies.backend import get_backend
from schemas.user import UserHeader
from .template import TemplateResponse, get_template_response
from .utils import hx_location


# class OAuth2CookiePasswordBearer(OAuth2PasswordBearer):
#     async def __call__(self, request: Request) -> str | None:
#         authorization = request.cookies.get("access_token")
#         scheme, param = get_authorization_scheme_param(authorization)
#         if not authorization or scheme.lower() != "bearer":
#             return None
#         return param


# oauth2_scheme = OAuth2CookiePasswordBearer(tokenUrl="auth/token", auto_error=False)


def unlogged() -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        headers=hx_location("/partial/unlogged", "#main-content"),
    )


async def require_login(backend: BackendService = Depends(get_backend)) -> UserHeader:
    try:
        return await backend.get_user()
    except NotAuthorizedError:
        unlogged()
