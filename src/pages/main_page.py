# from fastapi import Response
# from backend import BackendService
# from dependencies.template import TemplateResponse
# from pages.page import Page, PageType
# from schemas.user import UserHeader


# class MainPage(Page):
#     page_type = PageType.MAIN

#     def __init__(self, backend: BackendService) -> None:
#         super().__init__(backend)

#     async def get_response(
#         self, template_response: TemplateResponse, user: UserHeader
#     ) -> Response:
