from sqlalchemy.orm import Session

from backend.app.models.comment import Comment
from backend.app.schemas.comment import CommentCreate, CommentUpdate


def get_comments(
    db: Session
):
    return db.query(Comment).all()


def get_comment_by_id(
    db: Session,
    comment_id: int
):
    return db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

def incident_exists(
    db: Session,
    incident_id: int
):
    from backend.app.models.incident import Incident

    return db.query(Incident).filter(
        Incident.id == incident_id
    ).first() is not None


def user_exists(
    db: Session,
    user_id: int
):
    from backend.app.models.user import User

    return db.query(User).filter(
        User.id == user_id
    ).first() is not None


def create_comment(
    db: Session,
    comment_data: CommentCreate
):
    comment = Comment(
        incident_id=comment_data.incident_id,
        user_id=comment_data.user_id,
        comment=comment_data.comment
    )

    try:
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment

    except Exception:
        db.rollback()
        raise


def update_comment(
    db: Session,
    comment: Comment,
    comment_data: CommentUpdate
):
    if comment_data.comment is not None:
        comment.comment = comment_data.comment

    try:
        db.commit()
        db.refresh(comment)

        return comment

    except Exception:
        db.rollback()
        raise


def delete_comment(
    db: Session,
    comment: Comment
):
    try:
        db.delete(comment)
        db.commit()

    except Exception:
        db.rollback()
        raise