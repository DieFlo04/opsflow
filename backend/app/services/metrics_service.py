from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.models.incident import Incident


def get_incident_metrics(db: Session):
    total = db.query(func.count(Incident.id)).scalar()

    open_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "OPEN"
    ).scalar()

    in_progress_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "IN_PROGRESS"
    ).scalar()

    resolved_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "RESOLVED"
    ).scalar()

    closed_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status == "CLOSED"
    ).scalar()

    return {
        "total": total,
        "open": open_incidents,
        "in_progress": in_progress_incidents,
        "resolved": resolved_incidents,
        "closed": closed_incidents
    }


def get_incidents_by_priority(db: Session):
    results = db.query(
        Incident.priority,
        func.count(Incident.id)
    ).group_by(
        Incident.priority
    ).all()

    return {
        priority: count
        for priority, count in results
    }
    
    
def get_incidents_by_status(db: Session):
    results = db.query(
        Incident.status,
        func.count(Incident.id)
    ).group_by(
        Incident.status
    ).all()

    return {
        status: count
        for status, count in results
    }
    

def get_incidents_by_system(db: Session):
    from backend.app.models.system import System

    results = db.query(
        System.name,
        func.count(Incident.id)
    ).join(
        Incident,
        Incident.system_id == System.id
    ).group_by(
        System.name
    ).all()

    return {
        system_name: count
        for system_name, count in results
    }
    
def get_incidents_by_category(db: Session):
    from backend.app.models.category import Category

    results = db.query(
        Category.name,
        func.count(Incident.id)
    ).join(
        Incident,
        Incident.category_id == Category.id
    ).group_by(
        Category.name
    ).all()

    return {
        category_name: count
        for category_name, count in results
    }
    
    
def get_critical_incidents(db: Session):
    return db.query(Incident).filter(
        Incident.priority == "CRITICAL",
        Incident.status != "CLOSED"
    ).all()
    

def get_open_incidents(db: Session):
    return db.query(Incident).filter(
        Incident.status.in_(["OPEN", "IN_PROGRESS"])
    ).order_by(
        Incident.created_at.asc()
    ).all()
    
    
def get_incident_age(db: Session):
    incidents = db.query(Incident).filter(
        Incident.status.in_(["OPEN", "IN_PROGRESS"])
    ).order_by(
        Incident.created_at.asc()
    ).all()

    now = datetime.now(timezone.utc)

    results = []

    for incident in incidents:
        created_at = incident.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age = now - created_at

        results.append({
            "id": incident.id,
            "title": incident.title,
            "status": incident.status,
            "priority": incident.priority,
            "created_at": incident.created_at,
            "age_hours": round(age.total_seconds() / 3600, 2)
        })

    return results


def analyze_incidents(db: Session):
    critical_incidents = get_critical_incidents(db)
    open_incidents = get_open_incidents(db)
    old_incidents = get_old_incidents(db)

    alerts = []

    for incident in critical_incidents:
        alerts.append({
            "type": "CRITICAL_INCIDENT",
            "severity": "HIGH",
            "incident_id": incident.id,
            "message": (
                f"Critical incident requires attention: "
                f"{incident.title}"
            )
        })

    for incident in old_incidents:
        alerts.append({
            "type": "OLD_INCIDENT",
            "severity": "MEDIUM",
            "incident_id": incident["id"],
            "message": (
                f"Incident has been open for "
                f"{incident['age_hours']} hours: "
                f"{incident['title']}"
            )
        })

    return {
        "total_open_incidents": len(open_incidents),
        "critical_incidents": len(critical_incidents),
        "old_incidents": len(old_incidents),
        "alerts": alerts
    }
    
    
def get_old_incidents(
    db: Session,
    threshold_hours: int = 24
):
    incidents = get_open_incidents(db)

    now = datetime.now(timezone.utc)

    old_incidents = []

    for incident in incidents:
        created_at = incident.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age_hours = (
            now - created_at
        ).total_seconds() / 3600

        if age_hours >= threshold_hours:
            old_incidents.append({
                "id": incident.id,
                "title": incident.title,
                "status": incident.status,
                "priority": incident.priority,
                "age_hours": round(age_hours, 2)
            })

    return old_incidents


def get_resolved_incidents(db: Session):
    return db.query(Incident).filter(
        Incident.resolved_at.isnot(None)
    ).order_by(
        Incident.resolved_at.asc()
    ).all()
    
    
def get_resolution_times(db: Session):
    incidents = get_resolved_incidents(db)

    results = []

    for incident in incidents:
        created_at = incident.created_at
        resolved_at = incident.resolved_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if resolved_at.tzinfo is None:
            resolved_at = resolved_at.replace(tzinfo=timezone.utc)

        resolution_hours = (
            resolved_at - created_at
        ).total_seconds() / 3600

        results.append({
            "id": incident.id,
            "title": incident.title,
            "priority": incident.priority,
            "created_at": incident.created_at,
            "resolved_at": incident.resolved_at,
            "resolution_hours": round(resolution_hours, 2)
        })

    return results


def get_average_resolution_time(db: Session):
    incidents = get_resolved_incidents(db)

    if not incidents:
        return {
            "resolved_incidents": 0,
            "average_resolution_hours": 0
        }

    total_hours = 0

    for incident in incidents:
        created_at = incident.created_at
        resolved_at = incident.resolved_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if resolved_at.tzinfo is None:
            resolved_at = resolved_at.replace(tzinfo=timezone.utc)

        total_hours += (
            resolved_at - created_at
        ).total_seconds() / 3600

    average_hours = total_hours / len(incidents)

    return {
        "resolved_incidents": len(incidents),
        "average_resolution_hours": round(average_hours, 2)
    }