from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_user, crud_favorite
from app.core.config import settings
from app.schemas.user import UserCreate
from app.schemas.favorite import FavoriteCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.site import create_random_site


def test_get_users_user_me(
        client: TestClient, user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_new_user(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    name = "test"
    email = random_email()
    password = random_lower_string()
    data = {"name": name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud_user.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_create_user_existing_email(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    name = "test"
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(name=name, email=email, password=password)
    crud_user.user.create(db, obj_in=user_in)
    data = {"name": name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=user_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_update_user(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    name_updated = "test update"
    data = {"name": name_updated}
    r = client.put(
        f"{settings.API_V1_STR}/users/me", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    updated_user = r.json()
    user = crud_user.user.get_by_email(db, email=settings.EMAIL_TEST_USER)
    assert user
    assert user.name == updated_user["name"]


def test_create_user_favorite(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    user = crud_user.user.get_by_email(db, email=settings.EMAIL_TEST_USER)
    site = create_random_site(db)
    data = {"site_id": site.id}
    r = client.post(
        f"{settings.API_V1_STR}/users/me/favorites", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_favorite = r.json()
    favorite = crud_favorite.favorite.find_favorite(db, user_id=user.id, site_id=site.id)
    assert favorite
    assert favorite.user_id == created_favorite["user_id"]
    assert favorite.site_id == created_favorite["site_id"]


def test_delete_favorite(
     client: TestClient, user_token_headers: dict, db: Session
) -> None:
    user = crud_user.user.get_by_email(db, email=settings.EMAIL_TEST_USER)
    site = create_random_site(db)
    favorite = crud_favorite.favorite.create_favorite(db, obj_in=FavoriteCreate(site_id=site.id), user_id=user.id)

    assert favorite.site_id == site.id
    assert favorite.user_id == user.id

    r = client.delete(
        f"{settings.API_V1_STR}/users/me/favorites?site_id={site.id}", headers=user_token_headers
    )
    user_id = r.json()["user_id"]
    site_id = r.json()["site_id"]
    del_favorite = crud_favorite.favorite.find_favorite(db, user_id=user_id, site_id=site_id)
    assert del_favorite is None
