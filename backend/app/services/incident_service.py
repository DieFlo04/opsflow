import math
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from backend.app.models.incident import Incident
from backend.app.schemas.incident import IncidentCreate, IncidentUpdate

ALLOWED_STATUS_TRANSITIONS = {
    "OPEN": {"OPEN", "IN_PROGRESS"},
    "IN_PROGRESS": {"OPEN", "IN_PROGRESS", "RESOLVED"},
    "RESOLVED": {"RESOLVED", "IN_PROGRESS", "CLOSED"},
    "CLOSED": {"CLOSED", "IN_PROGRESS"},
}

ALLOWED_SORT_FIELDS = {
    "created_at": Incident.created_at,
    "updated_at": Incident.updated_at,
    "priority": Incident.priority,
    "status": Incident.status,
    "title": Incident.title,
}

ALLOWED_SORT_ORDERS = {"asc", "desc"}

def get_incidents(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    system_id: int | None = None,
    category_id: int | None = None,
    created_by: int | None = None,
    assigned_to: int | None = None,
    search: str | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
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
    
    if created_by is not None:
        query = query.filter(Incident.created_by == created_by)

    if assigned_to is not None:
        query = query.filter(Incident.assigned_to == assigned_to)
        
    if search is not None:
        search_term = f"%{search}%"

        query = query.filter(
            Incident.title.ilike(search_term)
            | Incident.description.ilike(search_term)
        )
        
    if created_from is not None:
        query = query.filter(
            Incident.created_at >= datetime.combine(created_from, datetime.min.time())
        )

    if created_to is not None:
        created_to_exclusive = datetime.combine(
            created_to + timedelta(days=1),
            datetime.min.time()
        )

        query = query.filter(
            Incident.created_at < created_to_exclusive
        )

    total = query.count()
    
    total_pages = math.ceil(total / page_size)

    offset = (page - 1) * page_size

    sort_column = ALLOWED_SORT_FIELDS.get(sort_by)

    if sort_column is None:
        raise ValueError(f"Invalid sort field: {sort_by}")

    if sort_order not in ALLOWED_SORT_ORDERS:
        raise ValueError(f"Invalid sort order: {sort_order}")

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    incidents = query.offset(offset).limit(page_size).all()

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