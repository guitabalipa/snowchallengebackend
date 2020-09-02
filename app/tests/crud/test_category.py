from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud import crud_category
from app.schemas.category import CategoryCreate
from app.tests.utils.utils import random_category_name
from app.tests.utils.category import create_random_category


def test_create_category(db: Session) -> None:
    name = random_category_name()
    category_in = CategoryCreate(name=name)
    category = crud_category.category.create(db, obj_in=category_in)
    assert category.name == name


def test_get_category(db: Session) -> None:
    category = create_random_category(db)

    category_2 = crud_category.category.get(db, id=category.id)

    assert category_2
    assert category.name == category_2.name
    assert jsonable_encoder(category.as_dict()) == jsonable_encoder(category_2.as_dict())


def test_get_category_by_name(db: Session) -> None:
    category = create_random_category(db)

    category_2 = crud_category.category.get_by_name(db, name=category.name)

    assert category_2
    assert category.name == category_2.name
    assert jsonable_encoder(category.as_dict()) == jsonable_encoder(category_2.as_dict())


def test_get_categories(db: Session) -> None:
    category = create_random_category(db)
    category_2 = create_random_category(db)

    categories = crud_category.category.get_multi(db)

    assert categories
    assert category in categories
    assert category_2 in categories
