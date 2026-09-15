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
    db: Session
):
    return db.query(Incident).all()


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
        new_status = incident_data.status.value

        allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
            incident.status,
            set()
        )

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Invalid status transition: "
                f"{incident.status} -> {new_status}"
            )

        incident.status = new_status

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