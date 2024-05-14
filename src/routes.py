from fastapi import APIRouter, Depends, Form, Response, status
from fastapi import HTTPException
from warnings import warn
from httpx import AsyncClient

from fastapi.responses import HTMLResponse

from dependencies.template import TemplateResponse, get_template_response
from dependencies.user import get_token

# from dependencies.user import get_logged_user, oauth2_scheme, get_auth_service
# from models.public import User
# from services.auth import AuthService, InvalidTokenError, TokenNotProvided

partial_router = APIRouter(prefix="/partial")

@partial_router.get("/content")
async def get_content(
    access_token: str | None = Depends(get_token),
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
    token: str = Depends(get_token),
) -> Response:
    return "Navbar"


@partial_router.get("/unlogged_navbar")
async def get_unlogged_navbar(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("unlogged_navbar.html")

@partial_router.post("/login")
async def login(login: str = Form(), password: str = Form()) -> None:
    return
    # response.set_cookie()