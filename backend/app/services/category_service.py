from sqlalchemy.orm import Session

from backend.app.models.category import Category
from backend.app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(
    db: Session
):
    return db.query(Category).all()


def get_category_by_id(
    db: Session,
    category_id: int
):
    return db.query(Category).filter(
        Category.id == category_id
    ).first()


def get_category_by_name(
    db: Session,
    name: str
):
    return db.query(Category).filter(
        Category.name == name
    ).first()


def create_category(
    db: Session,
    category_data: CategoryCreate
):
    category = Category(
        name=category_data.name
    )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    except Exception:
        db.rollback()
        raise


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryUpdate
):
    if category_data.name is not None:
        category.name = category_data.name

    try:
        db.commit()
        db.refresh(category)

        return category

    except Exception:
        db.rollback()
        raise


def delete_category(
    db: Session,
    category: Category
):
    try:
        db.delete(category)
        db.commit()

    except Exception:
        db.rollback()
        raise