from httpx import AsyncClient
from fastapi import status
from warnings import warn

from pydantic import TypeAdapter

from schemas.template import Template, TemplateCreate, TemplateHeader
from schemas.workspace import Workspace, WorkspaceCreate, WorkspaceHeader, UserHeader


class BackendError(BaseException):
    pass


class InvalidCredentialsError(BackendError):
    pass


class NotAuthorizedError(BackendError):
    pass


class WorkspaceCreateError(BackendError):
    pass


class BackendService:
    def __init__(self, http_client: AsyncClient) -> None:
        self.client = http_client

    async def login(self, username: str, password: str) -> str:
        response = await self.client.post(
            "/auth/token", data={"username": username, "password": password}
        )
        warn(response.content)
        if response.status_code == status.HTTP_200_OK:
            return response.json()["access_token"]
        raise InvalidCredentialsError()

    async def get_user(self) -> UserHeader:
        response = await self.client.get("/user/me")
        warn(response.status_code)
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
