from datetime import datetime

from pydantic import BaseModel


class PostSchema(BaseModel):
    text: str
    title: str | None = None


class PostResponseSchema(BaseModel):
    id: int
    title: str
    text: str
    created: datetime
    modified: datetime
    user_id: int
