import warnings
from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
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


async def get_token(
    access_token: str | None = Cookie(default=None),
) -> None:
    warnings.warn(str(access_token))
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            headers=hx_location("/partial/unlogged", "#main_content"),
        )
