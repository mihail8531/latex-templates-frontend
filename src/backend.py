from httpx import AsyncClient
from fastapi import status
from warnings import warn

from pydantic import SecretStr, TypeAdapter, ValidationError
import pydantic_core

from schemas.template import Template, TemplateCreate, TemplateHeader
from schemas.tickets_set import TicketsSet
from schemas.user import UserCreate
from schemas.workspace import Workspace, WorkspaceCreate, WorkspaceHeader, UserHeader


class BackendError(BaseException):
    pass


class InvalidCredentialsError(BackendError):
    pass


class NotAuthorizedError(BackendError):
    pass


class WorkspaceCreateError(BackendError):
    pass


class RegisterError(BackendError):
    pass


class AccountAlreadyExists(BackendError):
    pass


class AccountNotFound(BackendError):
    pass


class BackendService:
    def __init__(self, http_client: AsyncClient) -> None:
        self.client = http_client

    async def login(self, login: str, password: str) -> str:
        response = await self.client.post(
            "/auth/token", data={"username": login, "password": password}
        )
        if response.status_code == status.HTTP_200_OK:
            return response.json()["access_token"]
        raise InvalidCredentialsError()

    async def register(
        self, login: str, password: str, display_name: str, email: str
    ) -> None:
        user_create = UserCreate(
            login=login, email=email, display_name=display_name, password=password
        )
        response = await self.client.post("/user/create", json=user_create.model_dump())
        if response.status_code == status.HTTP_409_CONFLICT:
            raise AccountAlreadyExists()
        if response.status_code != status.HTTP_200_OK:
            raise RegisterError()

    async def get_user(self) -> UserHeader:
        response = await self.client.get("/user/me")
        if response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ):
            raise NotAuthorizedError()
        return UserHeader.model_validate_json(response.content)

    async def get_workspaces(self) -> list[WorkspaceHeader]:
        response = await self.client.get("/workspace/list")
        return TypeAdapter(list[WorkspaceHeader]).validate_json(response.content)

    async def get_workspace(self, workspace_id: int) -> Workspace:
        response = await self.client.get(f"/workspace/{workspace_id}")
        return Workspace.model_validate_json(response.content)

    async def create_workspace(self, workspace_create: WorkspaceCreate) -> None:
        response = await self.client.post(
            "/workspace/create", json=workspace_create.model_dump()
        )
        if response.status_code != status.HTTP_200_OK:
            raise WorkspaceCreateError()

    async def create_template(
        self, workspace_id: int, template_create: TemplateCreate
    ) -> TemplateHeader:
        response = await self.client.post(
            f"/workspace/{workspace_id}/template", json=template_create.model_dump()
        )
        return TemplateHeader.model_validate_json(response.content)

    async def get_template(self, workspace_id: int, template_id: int) -> Template:
        response = await self.client.get(
            f"/workspace/{workspace_id}/template/{template_id}"
        )
        return Template.model_validate_json(response.content)

    async def get_tickets_set(
        self, workspace_id: int, template_id: int, tickets_set_id: int
    ) -> TicketsSet:
        response = await self.client.get(
            f"/workspace/{workspace_id}/template/{template_id}/tickets_set/{tickets_set_id}"
        )
        return TicketsSet.model_validate_json(response.content)

    async def add_user_to_workspace(
        self, workspace_id: int, user_to_add_login: str
    ) -> None:
        response = await self.client.get("/user/", params={"login": user_to_add_login})
        if response.status_code != 200:
            raise AccountNotFound()
        user_to_add = UserHeader.model_validate_json(response.content)
        response = await self.client.post(
            f"/workspace/{workspace_id}/user/{user_to_add.id}"
        )
        if response.status_code == 409:
            raise AccountAlreadyExists()

    async def update_template(
        self,
        workspace_id: int,
        template_id: int,
        name: str,
        description: str | None,
        latex: str,
        lua: str,
    ) -> None:
        response = await self.client.put(
            f"/workspace/{workspace_id}/template/{template_id}",
            json=TemplateCreate(
                name=name, description=description, latex=latex, lua_example=lua
            ).model_dump(),
        )
