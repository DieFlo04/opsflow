from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.incident import Incident
from backend.app.models.user import User
from backend.app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentListResponse,
    IncidentPriority,
    IncidentStatus
)
from backend.app.services.incident_service import (
    category_exists,
    create_incident,
    delete_incident,
    get_incident_by_id,
    get_incidents,
    system_exists,
    update_incident,
    user_exists
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.get("/", response_model=IncidentListResponse)
def list_incidents(
    status: IncidentStatus | None = None,
    priority: IncidentPriority | None = None,
    system_id: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
        return get_incidents(
        db,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        system_id=system_id,
        category_id=category_id,
        search=search,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.post(
    "/",
    response_model=IncidentResponse
)
def create_new_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not system_exists(
        db,
        incident_data.system_id
    ):
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    if not category_exists(
        db,
        incident_data.category_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if not user_exists(
        db,
        incident_data.created_by
    ):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return create_incident(
        db,
        incident_data
    )


@router.put(
    "/{incident_id}",
    response_model=IncidentResponse
)
def update_existing_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("technician", "admin")
    )
):
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    if incident_data.system_id is not None:
        if not system_exists(
            db,
            incident_data.system_id
        ):
            raise HTTPException(
                status_code=404,
                detail="System not found"
            )

    if incident_data.category_id is not None:
        if not category_exists(
            db,
            incident_data.category_id
        ):
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if incident_data.assigned_to is not None:
        if not user_exists(
            db,
            incident_data.assigned_to
        ):
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    try:
        return update_incident(
            db,
            incident,
            incident_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete(
    "/{incident_id}"
)
def delete_existing_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    delete_incident(
        db,
        incident
    )

    return {
        "message": "Incident deleted successfully"
    }