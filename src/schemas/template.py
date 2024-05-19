from datetime import datetime
from pydantic import BaseModel
from .tickets_set import TicketsSetHeader


class TemplateBase(BaseModel):
    name: str
    description: str | None
    latex: str | None
    lua_example: str | None


class TemplateCreate(TemplateBase):
    pass


class TemplateHeader(TemplateBase):
    id: int
    author_id: int
    workspace_id: int
    creation_timestamp: datetime


class Template(TemplateHeader):
    tickets_sets: list[TicketsSetHeader]
