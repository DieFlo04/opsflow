from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.incident import Incident
from backend.app.models.user import User
from backend.app.models.system import System
from backend.app.models.category import Category
from backend.app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse
)
from backend.app.services.incident_service import (
    create_incident,
    delete_incident,
    get_incident_by_id,
    get_incidents,
    update_incident
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.get(
    "/",
    response_model=list[IncidentResponse]
)
def list_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incidents(db)


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
    system = db.query(System).filter(
        System.id == incident_data.system_id
    ).first()

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    category = db.query(Category).filter(
        Category.id == incident_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    user = db.query(User).filter(
        User.id == incident_data.created_by
    ).first()

    if not user:
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
        system = db.query(System).filter(
            System.id == incident_data.system_id
        ).first()

        if not system:
            raise HTTPException(
                status_code=404,
                detail="System not found"
            )

    if incident_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == incident_data.category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if incident_data.assigned_to is not None:
        user = db.query(User).filter(
            User.id == incident_data.assigned_to
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
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