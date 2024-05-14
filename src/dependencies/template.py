from functools import cache
from typing import Any, Callable, TypeAlias, Protocol, Mapping
from fastapi import Depends, Request, Response
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from dependencies.settings import settings_t
from settings import AppSettings


# TemplateResponse: TypeAlias = Callable[[str, dict[str, Any] | None], Response]


def get_templates(
    settings: AppSettings = Depends(settings_t(AppSettings)),
) -> Jinja2Templates:
    return Jinja2Templates(settings.TEMPLATES_PATH)


class TemplateResponse(Protocol):
    def __call__(
        self,
        name: str,
        data: dict[str, Any] | None = ...,
        status_code: int = ...,
        headers: Mapping[str, str] | None = ...,
        media_type: str | None = ...,
        background: BackgroundTask | None = ...,
    ) -> Response: ...


def get_template_response(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
) -> TemplateResponse:
    def template_response(
        name: str,
        data: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> Response:
        if data is None:
            data = dict()
        return templates.TemplateResponse(
            name,
            {"request": request, **data},
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    return template_response
