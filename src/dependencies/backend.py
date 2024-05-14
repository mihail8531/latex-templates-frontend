from fastapi import Depends
from httpx import AsyncClient
from backend import BackendService
from request import get_http_client
from settings import BackendSettings
from .settings import settings_t


def get_backend(
    http_client: AsyncClient = Depends(get_http_client),
    settings: BackendSettings = Depends(settings_t(BackendSettings)),
) -> BackendService:
    return BackendService(http_client)
