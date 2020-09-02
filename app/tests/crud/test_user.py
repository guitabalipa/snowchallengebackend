from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import create_random_user
from app.core.security import verify_password


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    name = "test"
    user_in = UserCreate(name=name, email=email, password=password)
    user = crud_user.user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_get_user_by_email(db: Session) -> None:
    user = create_random_user(db)
    user_2 = crud_user.user.get_by_email(db, email=user.email)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user.as_dict()) == jsonable_encoder(user_2.as_dict())


def test_get_user(db: Session) -> None:
    user = create_random_user(db)
    user_2 = crud_user.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user.as_dict()) == jsonable_encoder(user_2.as_dict())


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    name = "test"
    user_in = UserCreate(name=name, email=email, password=password)
    user = crud_user.user.create(db, obj_in=user_in)
    authenticated_user = crud_user.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud_user.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    user = create_random_user(db)
    is_active = crud_user.user.is_active(user)
    assert is_active is True


def test_update_user(db: Session) -> None:
    user = create_random_user(db)
    new_password = random_lower_string()
    user_in_update = UserUpdate(name=user.name, email=user.email, password=new_password)
    crud_user.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud_user.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
