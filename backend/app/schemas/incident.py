from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class IncidentPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentCreate(BaseModel):
    title: str
    description: str
    priority: IncidentPriority = IncidentPriority.MEDIUM
    system_id: int
    category_id: int
    created_by: int


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: IncidentPriority | None = None
    status: IncidentStatus | None = None
    system_id: int | None = None
    category_id: int | None = None
    assigned_to: int | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: IncidentPriority
    status: IncidentStatus
    system_id: int
    category_id: int
    created_by: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)