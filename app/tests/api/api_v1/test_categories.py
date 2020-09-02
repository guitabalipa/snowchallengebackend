from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_category
from app.core.config import settings
from app.tests.utils.utils import random_category_name


def test_create_new_category(
        client: TestClient, user_token_headers: dict, db: Session
) -> None:
    name = random_category_name()
    data = {"name": name}
    r = client.post(
        f"{settings.API_V1_STR}/categories/", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_category = r.json()
    category = crud_category.category.get_by_name(db, name=name)
    assert category
    assert category.name == created_category["name"]
