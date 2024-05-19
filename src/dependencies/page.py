from fastapi import Cookie, Depends

from backend import BackendService
from dependencies.backend import get_backend
from dependencies.state import state
from pages.page import Page, PageType
from pages.registry import PageRegistry


def get_page_type(page: str | None = Cookie(None)) -> PageType:
    if not PageType.has_value(page):
        return PageType.MAIN
    return PageType(page)


def get_page_registry(
    registry: PageRegistry = Depends(state("page_registry")),
) -> PageRegistry:
    return registry


def get_page(
    page_type: PageType = Depends(get_page_type),
    page_registry: PageRegistry = Depends(get_page_registry),
    backend: BackendService = Depends(get_backend),
) -> Page:
    return page_registry[page_type](backend)
