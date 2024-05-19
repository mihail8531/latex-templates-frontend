from pydantic import BaseModel, HttpUrl
from datetime import datetime


class TicketsSetBase(BaseModel):
    name: str
    description: str | None


class TicketsSetHeader(TicketsSetBase):
    id: int
    author_id: int
    template_id: int
    creation_timestamp: datetime


class TicketsSet(TicketsSetHeader):
    pdf_url: HttpUrl
