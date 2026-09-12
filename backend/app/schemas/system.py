from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SystemCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "ACTIVE"


class SystemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None


class SystemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)