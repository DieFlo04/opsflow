from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, UserUpdate
from backend.app.services.user_service import (
    create_user,
    delete_user,
    email_exists,
    get_user_by_id,
    get_users,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse]
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.post(
    "/",
    response_model=UserResponse
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    if email_exists(
    db,
    user_data.email
):
        raise HTTPException(
        status_code=400,
        detail="Email already registered"
    )

    return create_user(
        db,
        user_data
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_data.email is not None:
        if email_exists(
            db,
            user_data.email,
            exclude_user_id=user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    return update_user(
        db,
        user,
        user_data
    )


@router.delete(
    "/{user_id}"
)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    delete_user(
        db,
        user
    )

    return {
        "message": "User deleted successfully"
    }