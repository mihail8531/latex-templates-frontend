from fastapi import Cookie, Depends
from httpx import AsyncClient, Auth

from dependencies.settings import settings_t
from settings import BackendSettings


class TokenAuth(Auth):
    requires_response_body = True

    def __init__(self, access_token: str | None) -> None:
        self.access_token = access_token

    def auth_flow(self, request):
        if self.access_token is not None:
            request.headers["Authorization"] = f"Bearer {self.access_token}"
        yield request


def get_http_client(
    settings: BackendSettings = Depends(settings_t(BackendSettings)),
    access_token: str | None = Cookie(None),
) -> AsyncClient:
    return AsyncClient(base_url=settings.REST_URL, auth=TokenAuth(access_token))
