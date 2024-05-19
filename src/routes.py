from fastapi import APIRouter, Depends, Form, Response, status
from fastapi import HTTPException
from warnings import warn
from httpx import AsyncClient

from fastapi.responses import HTMLResponse

from backend import BackendService, InvalidCredentialsError, WorkspaceCreateError
from dependencies.template import TemplateResponse, get_template_response
from dependencies.user import require_login
from dependencies.backend import get_backend
from schemas.template import TemplateCreate
from schemas.user import UserBase, UserHeader
from schemas.workspace import WorkspaceCreate

# from dependencies.user import get_logged_user, oauth2_scheme, get_auth_service
# from models.public import User
# from services.auth import AuthService, InvalidTokenError, TokenNotProvided
partial_router = APIRouter(prefix="/partial")


@partial_router.get("/content")
async def get_content(
    user: UserHeader = Depends(require_login),
    template_response: TemplateResponse = Depends(get_template_response),
    backend: BackendService = Depends(get_backend),
) -> Response:
    workspaces = await backend.get_workspaces()
    return template_response(
        "main.jinja", data={"workspaces": workspaces, "user": user.model_dump()}
    )


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
    warn(workspace.model_dump_json())
    return template_response(
        "workspace_info.jinja", data={"workspace": workspace.model_dump()}
    )


@partial_router.get("/create_workspace_form")
async def get_create_workspace_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("create_workspace_form.html")


@partial_router.post("/create_workspace")
async def create_workspace(
    name: str = Form(default=""),
    description: str = Form(default=""),
    backend: BackendService = Depends(get_backend),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    workspace_create = WorkspaceCreate(name=name, description=description)
    try:
        await backend.create_workspace(workspace_create)
    except WorkspaceCreateError:
        return template_response("workspace_create_error.html")

    return template_response("logged.html")


@partial_router.get("/create_template_form")
async def get_create_template_form(
    workspace_id: int,
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response(
        "create_template_form.jinja", data={"workspace_id": workspace_id}
    )


@partial_router.post("/create_template")
async def create_template(
    workspace_id: int,
    name: str = Form(default=""),
    description: str = Form(default=""),
    backend: BackendService = Depends(get_backend),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    template_create = TemplateCreate(
        name=name.strip(), description=description.strip(), latex="", lua_example=""
    )
    template = await backend.create_template(workspace_id, template_create)
    workspace = await backend.get_workspace(workspace_id)
    if template.id not in workspace.template_ids:
        workspace.templates.append(template)
    return template_response(
        "workspace_info.jinja", data={"workspace": workspace.model_dump()}
    )


@partial_router.get("/workspace/{workspace_id}/template/{template_id}")
async def get_template_page(
    workspace_id: int,
    template_id: int,
    backend: BackendService = Depends(get_backend),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    template = await backend.get_template(workspace_id, template_id)
    return template_response("template.jinja", data={"template": template.model_dump()})
