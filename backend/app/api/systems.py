from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.system import System
from backend.app.schemas.system import (
    SystemCreate,
    SystemUpdate,
    SystemResponse
)


router = APIRouter(
    prefix="/systems",
    tags=["Systems"]
)


@router.post("/", response_model=SystemResponse)
def create_system(
    system_data: SystemCreate,
    db: Session = Depends(get_db)
):
    existing_system = db.query(System).filter(
        System.name == system_data.name
    ).first()

    if existing_system:
        raise HTTPException(
            status_code=400,
            detail="System already exists"
        )

    system = System(
        name=system_data.name,
        description=system_data.description,
        status=system_data.status
    )

    db.add(system)
    db.commit()
    db.refresh(system)

    return system


@router.get("/", response_model=list[SystemResponse])
def get_systems(
    db: Session = Depends(get_db)
):
    systems = db.query(System).all()

    return systems


@router.get("/{system_id}", response_model=SystemResponse)
def get_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    system = db.query(System).filter(
        System.id == system_id
    ).first()

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    return system


@router.put("/{system_id}", response_model=SystemResponse)
def update_system(
    system_id: int,
    system_data: SystemUpdate,
    db: Session = Depends(get_db)
):
    system = db.query(System).filter(
        System.id == system_id
    ).first()

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    update_data = system_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        existing_system = db.query(System).filter(
            System.name == update_data["name"],
            System.id != system_id
        ).first()

        if existing_system:
            raise HTTPException(
                status_code=400,
                detail="System already exists"
            )

    for field, value in update_data.items():
        setattr(system, field, value)

    db.commit()
    db.refresh(system)

    return system


@router.delete("/{system_id}")
def delete_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    system = db.query(System).filter(
        System.id == system_id
    ).first()

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    db.delete(system)
    db.commit()

    return {
        "message": "System deleted successfully"
    }