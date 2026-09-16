from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.services.metrics_service import (
    get_incident_metrics,
    get_incidents_by_priority,
    get_incidents_by_status,
    get_incidents_by_system,
    get_incidents_by_category,
    get_critical_incidents,
    get_open_incidents,
    get_incident_age,
    analyze_incidents,
    get_old_incidents,
    get_resolved_incidents,
    get_resolution_times,
    get_average_resolution_time
)


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("/incidents")
def incident_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incident_metrics(db)


@router.get("/incidents/by-priority")
def incidents_by_priority(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incidents_by_priority(db)


@router.get("/incidents/by-status")
def incidents_by_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incidents_by_status(db)


@router.get("/incidents/by-system")
def incidents_by_system(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incidents_by_system(db)


@router.get("/incidents/by-category")
def incidents_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incidents_by_category(db)


@router.get("/incidents/critical")
def critical_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_critical_incidents(db)


@router.get("/incidents/open")
def open_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_open_incidents(db)


@router.get("/incidents/age")
def incident_age(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incident_age(db)


@router.get("/analysis")
def incident_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return analyze_incidents(db)


@router.get("/incidents/resolution-times")
def resolution_times(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_resolution_times(db)


@router.get("/incidents/average-resolution-time")
def average_resolution_time(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_average_resolution_time(db)