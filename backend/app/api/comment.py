from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.comment import Comment
from backend.app.models.incident import Incident
from backend.app.models.user import User
from backend.app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse
)
from backend.app.services.comment_service import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments,
    update_comment
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get(
    "/",
    response_model=list[CommentResponse]
)
def list_comments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_comments(db)


@router.get(
    "/{comment_id}",
    response_model=CommentResponse
)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment


@router.post(
    "/",
    response_model=CommentResponse
)
def create_new_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = db.query(Incident).filter(
        Incident.id == comment_data.incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    user = db.query(User).filter(
        User.id == comment_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return create_comment(
        db,
        comment_data
    )


@router.put(
    "/{comment_id}",
    response_model=CommentResponse
)
def update_existing_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("technician", "admin")
    )
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return update_comment(
        db,
        comment,
        comment_data
    )


@router.delete(
    "/{comment_id}"
)
def delete_existing_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    delete_comment(
        db,
        comment
    )

    return {
        "message": "Comment deleted successfully"
    }