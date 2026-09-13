from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role

from backend.app.models.incident import Incident
from backend.app.models.system import System
from backend.app.models.category import Category
from backend.app.models.user import User

from backend.app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse
)

ALLOWED_STATUS_TRANSITIONS = {
    "OPEN": {"OPEN", "IN_PROGRESS"},
    "IN_PROGRESS": {"OPEN", "IN_PROGRESS", "RESOLVED"},
    "RESOLVED": {"RESOLVED", "IN_PROGRESS", "CLOSED"},
    "CLOSED": {"CLOSED", "IN_PROGRESS"}
}

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=IncidentResponse)
def create_incident(
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

    creator = db.query(User).filter(
        User.id == incident_data.created_by
    ).first()

    if not creator:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        priority=incident_data.priority,
        system_id=incident_data.system_id,
        category_id=incident_data.category_id,
        created_by=incident_data.created_by
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incidents = db.query(Incident).all()
    
    return incidents


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )
    
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
    require_role("technician", "admin")
)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    update_data = incident_data.model_dump(
        exclude_unset=True
    )

    if "system_id" in update_data:
        system = db.query(System).filter(
            System.id == update_data["system_id"]
        ).first()

        if not system:
            raise HTTPException(
                status_code=404,
                detail="System not found"
            )

    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"]
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if "assigned_to" in update_data:
        if update_data["assigned_to"] is not None:
            user = db.query(User).filter(
                User.id == update_data["assigned_to"]
            ).first()

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="Assigned user not found"
                )

    if "status" in update_data:
        current_status = incident.status
        new_status = update_data["status"]

        allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
            current_status,
            set()
        )

        if new_status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid status transition: "
                    f"{current_status} -> {new_status}"
                )
            )

        if new_status == "RESOLVED":
            if incident.resolved_at is None:
                incident.resolved_at = datetime.utcnow()
        else:
            incident.resolved_at = None

    for field, value in update_data.items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)

    return incident


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
    require_role("admin")
    )
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return {
        "message": "Incident deleted successfully"
    }