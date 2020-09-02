from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_site, crud_category
from app.core.config import settings
from app.tests.utils.utils import random_site_name, random_category_name
from app.tests.utils.category import create_random_category
from app.schemas.category import CategoryCreate
from app.schemas.site import SiteCreate
from app.tests.utils.site import create_random_site


def test_create_site(
        client: TestClient, user_token_headers: Dict[str, str], db: Session
) -> None:
    name = random_site_name()
    latitude = "234234234"
    longitude = "234234234"
    category_id = create_random_category(db).id

    data = {"name": name, "lat": latitude, "lon": longitude, "category_id": category_id}
    r = client.post(
        f"{settings.API_V1_STR}/sites/", headers=user_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_site = r.json()
    site = crud_site.site.get_by_name(db, name=name)
    assert site
    assert site.name == created_site["name"]


# def test_update_site(
#         client: TestClient, user_token_headers: dict, db: Session
# ) -> None:
#     site_created = create_random_site(db)
#     name_updated = f"Update {random_site_name()}"
#     data = {"name": name_updated, "lat": site_created.lat, "lon": site_created.lon}
#     r = client.put(
#         f"{settings.API_V1_STR}/sites/{site_created.id}/", headers=user_token_headers, json=data,
#     )
#     assert 200 <= r.status_code < 300
#     updated_site = r.json()
#     site = crud_site.site.get(db, id=site_created.id)
#     assert site
#     assert site.name == updated_site["name"]
