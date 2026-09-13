from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.user import User
from backend.app.schemas.system import (
    SystemCreate,
    SystemResponse,
    SystemUpdate
)
from backend.app.services.system_service import (
    create_system,
    delete_system,
    get_system_by_id,
    get_system_by_name,
    get_systems,
    update_system
)

router = APIRouter(
    prefix="/systems",
    tags=["Systems"]
)


@router.get(
    "/",
    response_model=list[SystemResponse]
)
def list_systems(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_systems(db)


@router.get(
    "/{system_id}",
    response_model=SystemResponse
)
def get_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    system = get_system_by_id(
        db,
        system_id
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    return system


@router.post(
    "/",
    response_model=SystemResponse
)
def create_new_system(
    system_data: SystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    existing_system = get_system_by_name(
        db,
        system_data.name
    )

    if existing_system:
        raise HTTPException(
            status_code=400,
            detail="System already exists"
        )

    return create_system(
        db,
        system_data
    )


@router.put(
    "/{system_id}",
    response_model=SystemResponse
)
def update_existing_system(
    system_id: int,
    system_data: SystemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    system = get_system_by_id(
        db,
        system_id
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    if system_data.name is not None:
        existing_system = get_system_by_name(
            db,
            system_data.name
        )

        if (
            existing_system
            and existing_system.id != system_id
        ):
            raise HTTPException(
                status_code=400,
                detail="System already exists"
            )

    return update_system(
        db,
        system,
        system_data
    )


@router.delete(
    "/{system_id}"
)
def delete_existing_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    system = get_system_by_id(
        db,
        system_id
    )

    if not system:
        raise HTTPException(
            status_code=404,
            detail="System not found"
        )

    delete_system(
        db,
        system
    )

    return {
        "message": "System deleted successfully"
    }