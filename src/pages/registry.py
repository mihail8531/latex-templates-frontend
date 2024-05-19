from typing import Iterable
from pages.page import Page, PageType


class PageRegistry(dict[PageType, type[Page]]):

    def __init__(self, page_classes: Iterable[type[Page]]) -> None:
        super().__init__(
            [(page_class.page_type, page_class) for page_class in page_classes]
        )

    def set_page(self, page_class: type[Page]) -> None:
        self[page_class.page_type] = page_class
