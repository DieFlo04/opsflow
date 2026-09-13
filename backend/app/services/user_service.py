from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate
from backend.app.core.security import hash_password


def get_user_by_id(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_user_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_users(
    db: Session
):
    return db.query(User).all()


def create_user(
    db: Session,
    user_data: UserCreate
):
    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user: User,
    user_data: UserUpdate
):
    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    if user_data.password is not None:
        user.password_hash = hash_password(
            user_data.password
        )

    if user_data.role is not None:
        user.role = user_data.role

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()