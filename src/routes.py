from fastapi import APIRouter, Depends, Form, Response, status
from fastapi import HTTPException
from warnings import warn
from httpx import AsyncClient

from fastapi.responses import HTMLResponse

from backend import BackendService, InvalidCredentialsError
from dependencies.page import get_page
from dependencies.template import TemplateResponse, get_template_response
from dependencies.user import require_login
from dependencies.backend import get_backend
from pages.page import Page, PageType
from schemas.user import UserBase, UserHeader

# from dependencies.user import get_logged_user, oauth2_scheme, get_auth_service
# from models.public import User
# from services.auth import AuthService, InvalidTokenError, TokenNotProvided
partial_router = APIRouter(prefix="/partial")


@partial_router.get("/content")
async def get_content(
    user: UserHeader = Depends(require_login),
    page: Page = Depends(get_page),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return await page.get_response(template_response, user)


@partial_router.get("/register_form")
async def get_register_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("register_form.jinja")


@partial_router.get("/login_form")
async def get_login_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("login_form.html")


@partial_router.get("/unlogged")
async def get_unlogged(
    logout: bool = False,
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    response = template_response("unlogged.html")
    response.delete_cookie("access_token")
    return response


@partial_router.get("/navbar")
async def get_navbar(
    user: UserHeader = Depends(require_login),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("logged_navbar.jinja", data={"user": user.model_dump()})


@partial_router.get("/unlogged_navbar")
async def get_unlogged_navbar(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("unlogged_navbar.html")


@partial_router.post("/login")
async def login(
    response: Response,
    login: str = Form(default=""),
    password: str = Form(default=""),
    backend: BackendService = Depends(get_backend),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    try:
        token = await backend.login(login, password)
        response = template_response("logged.html")
        response.set_cookie("access_token", token)
        return response
    except InvalidCredentialsError:
        return template_response("login_error.html")


@partial_router.get("/workspace/{workspace_id}")
async def get_workspace_info(
    workspace_id: int,
    template_response: TemplateResponse = Depends(get_template_response),
    backend: BackendService = Depends(get_backend),
) -> Response:
    workspace = await backend.get_workspace(workspace_id)
    return template_response(
        "workspace_info.jinja", data={"workspace": workspace.model_dump()}
    )


@partial_router.get("/create_workspace_form")
async def get_create_workspace_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("create_workspace_form.html")
