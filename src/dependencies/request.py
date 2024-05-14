from fastapi import Depends
from httpx import AsyncClient

from dependencies.settings import get_backend_settings
from settings import BackendSettings


def get_http_client(
    settings: BackendSettings = Depends(get_backend_settings),
) -> AsyncClient:
    return AsyncClient(base_url=settings.REST_URL)
