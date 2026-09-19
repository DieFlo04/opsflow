import math
from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models.incident import Incident
from backend.app.schemas.incident import IncidentCreate, IncidentUpdate

ALLOWED_STATUS_TRANSITIONS = {
    "OPEN": {"OPEN", "IN_PROGRESS"},
    "IN_PROGRESS": {"OPEN", "IN_PROGRESS", "RESOLVED"},
    "RESOLVED": {"RESOLVED", "IN_PROGRESS", "CLOSED"},
    "CLOSED": {"CLOSED", "IN_PROGRESS"},
}


def get_incidents(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    system_id: int | None = None,
    category_id: int | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Incident)

    if status is not None:
        query = query.filter(Incident.status == status)

    if priority is not None:
        query = query.filter(Incident.priority == priority)

    if system_id is not None:
        query = query.filter(Incident.system_id == system_id)

    if category_id is not None:
        query = query.filter(Incident.category_id == category_id)
        
    if search is not None:
        search_term = f"%{search}%"

        query = query.filter(
            Incident.title.ilike(search_term)
            | Incident.description.ilike(search_term)
        )

    total = query.count()
    
    total_pages = math.ceil(total / page_size)

    offset = (page - 1) * page_size

    incidents = query.order_by(
        Incident.created_at.desc()
    ).offset(offset).limit(page_size).all()

    return {
    "items": incidents,
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
}


def get_incident_by_id(
    db: Session,
    incident_id: int
):
    return db.query(Incident).filter(
        Incident.id == incident_id
    ).first()


def system_exists(
    db: Session,
    system_id: int
):
    from backend.app.models.system import System

    return db.query(System).filter(
        System.id == system_id
    ).first() is not None


def category_exists(
    db: Session,
    category_id: int
):
    from backend.app.models.category import Category

    return db.query(Category).filter(
        Category.id == category_id
    ).first() is not None


def user_exists(
    db: Session,
    user_id: int
):
    from backend.app.models.user import User

    return db.query(User).filter(
        User.id == user_id
    ).first() is not None


def create_incident(
    db: Session,
    incident_data: IncidentCreate
):
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        priority=incident_data.priority.value,
        system_id=incident_data.system_id,
        category_id=incident_data.category_id,
        created_by=incident_data.created_by
    )

    try:
        db.add(incident)
        db.commit()
        db.refresh(incident)

        return incident

    except Exception:
        db.rollback()
        raise


def update_incident(
    db: Session,
    incident: Incident,
    incident_data: IncidentUpdate
):
    if incident_data.title is not None:
        incident.title = incident_data.title

    if incident_data.description is not None:
        incident.description = incident_data.description

    if incident_data.priority is not None:
        incident.priority = incident_data.priority.value

    if incident_data.system_id is not None:
        incident.system_id = incident_data.system_id

    if incident_data.category_id is not None:
        incident.category_id = incident_data.category_id

    if incident_data.assigned_to is not None:
        incident.assigned_to = incident_data.assigned_to

    if incident_data.status is not None:
        old_status = incident.status
        new_status = incident_data.status.value

        allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
            old_status,
            set()
        )

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Invalid status transition: "
                f"{old_status} -> {new_status}"
            )

        incident.status = new_status

        if new_status == "RESOLVED":
            incident.resolved_at = datetime.utcnow()

        elif old_status == "RESOLVED":
            incident.resolved_at = None

    try:
        db.commit()
        db.refresh(incident)

        return incident

    except Exception:
        db.rollback()
        raise


def delete_incident(
    db: Session,
    incident: Incident
):
    try:
        db.delete(incident)
        db.commit()

    except Exception:
        db.rollback()
        raise