from enum import Enum
from typing import Any, ClassVar, Protocol

from fastapi import Response

from backend import BackendService
from dependencies.template import TemplateResponse
from schemas.user import UserHeader


class PageType(Enum):
    MAIN = "main"
    WORKSPACE = "workspace"
    TEMPLATE = "template"

    @classmethod
    def has_value(cls, value: Any) -> bool:
        return value in cls._value2member_map_


class Page(Protocol):
    page_type: ClassVar[PageType]
    backend: BackendService

    def __init__(self, backend: BackendService) -> None:
        self.backend = backend

    async def get_response(self, template_response: TemplateResponse, user: UserHeader) -> Response: ...
