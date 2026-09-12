from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    incident_id: int
    user_id: int
    comment: str


class CommentUpdate(BaseModel):
    comment: str | None = None


class CommentResponse(BaseModel):
    id: int
    incident_id: int
    user_id: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)