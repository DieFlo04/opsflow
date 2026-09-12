from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.comment import Comment
from backend.app.models.incident import Incident
from backend.app.models.user import User
from backend.app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.post("/", response_model=CommentResponse)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db)
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

    comment = Comment(
        incident_id=comment_data.incident_id,
        user_id=comment_data.user_id,
        comment=comment_data.comment
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.get("/", response_model=list[CommentResponse])
def get_comments(
    db: Session = Depends(get_db)
):
    comments = db.query(Comment).all()
    
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    update_data = comment_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db.delete(comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }