from sqlalchemy.orm import Session

from app.tests.utils.utils import random_category_name
from app.crud import crud_category
from app.schemas.category import CategoryCreate


def create_random_category(db: Session):
    name = random_category_name()
    category_in = CategoryCreate(name=name)
    return crud_category.category.create(db, obj_in=category_in)
