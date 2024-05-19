from pydantic import BaseModel
from schemas.user import UserHeader, UserHeader
from datetime import datetime
from .template import TemplateHeader


class WorkspaceBase(BaseModel):
    name: str
    description: str


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceHeader(WorkspaceBase):
    id: int
    creation_timestamp: datetime


class Workspace(WorkspaceHeader):
    creator: UserHeader
    admin: UserHeader
    users: list[UserHeader]
    templates: list[TemplateHeader]

    @property
    def template_ids(self) -> set[int]:
        res = set()
        for template in self.templates:
            res.add(template.id)
        return res
