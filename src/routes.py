from fastapi import APIRouter, Depends, Form, Response, status
from fastapi import HTTPException
from warnings import warn
from httpx import AsyncClient

from fastapi.responses import HTMLResponse

from backend import BackendService, InvalidCredentialsError
from dependencies.template import TemplateResponse, get_template_response
from dependencies.user import require_login
from dependencies.backend import get_backend

# from dependencies.user import get_logged_user, oauth2_scheme, get_auth_service
# from models.public import User
# from services.auth import AuthService, InvalidTokenError, TokenNotProvided
partial_router = APIRouter(prefix="/partial")


@partial_router.get("/content")
async def get_content(
    logged: None = Depends(require_login),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("app.html")


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
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("unlogged.html")


@partial_router.get("/navbar")
async def get_navbar(
    logged: None = Depends(require_login),
) -> Response:
    return "Navbar"


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
