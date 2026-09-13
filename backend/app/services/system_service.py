from sqlalchemy.orm import Session

from backend.app.models.system import System
from backend.app.schemas.system import SystemCreate, SystemUpdate


def get_systems(
    db: Session
):
    return db.query(System).all()


def get_system_by_id(
    db: Session,
    system_id: int
):
    return db.query(System).filter(
        System.id == system_id
    ).first()


def get_system_by_name(
    db: Session,
    name: str
):
    return db.query(System).filter(
        System.name == name
    ).first()


def create_system(
    db: Session,
    system_data: SystemCreate
):
    system = System(
        name=system_data.name,
        description=system_data.description,
        status=system_data.status.value
        if hasattr(system_data.status, "value")
        else system_data.status
    )

    db.add(system)
    db.commit()
    db.refresh(system)

    return system


def update_system(
    db: Session,
    system: System,
    system_data: SystemUpdate
):
    if system_data.name is not None:
        system.name = system_data.name

    if system_data.description is not None:
        system.description = system_data.description

    if system_data.status is not None:
        system.status = (
            system_data.status.value
            if hasattr(system_data.status, "value")
            else system_data.status
        )

    db.commit()
    db.refresh(system)

    return system


def delete_system(
    db: Session,
    system: System
):
    db.delete(system)
    db.commit()