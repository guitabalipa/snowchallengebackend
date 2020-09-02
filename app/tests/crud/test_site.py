from sqlalchemy.orm import Session

from app.crud import crud_site, crud_category
from app.schemas.site import SiteCreate, SiteUpdate
from app.schemas.category import CategoryCreate
from app.tests.utils.utils import random_site_name, random_category_name
from app.tests.utils.site import create_random_site


def test_create_site(db: Session) -> None:
    cat_name = random_category_name()
    category_in = CategoryCreate(name=cat_name)
    category = crud_category.category.create(db, obj_in=category_in)
    name = random_site_name()
    lat = "78797979"
    lon = "76876868"
    site_in = SiteCreate(name=name, lat=lat, lon=lon, category_id=category.id)
    site = crud_site.site.create(db, obj_in=site_in)
    assert site.name == name
    assert site.lat == lat
    assert site.lon == lon
    assert site.category_id == category.id


def test_update_site(db: Session) -> None:
    site = create_random_site(db)
    new_name = random_site_name()
    site_in_update = SiteUpdate(name=new_name, lat=site.lat, lon=site.lon)
    crud_site.site.update(db, db_obj=site, obj_in=site_in_update)
    site_2 = crud_site.site.get(db, id=site.id)
    assert site_2
    assert site.name == site_2.name


def test_get_sites(db: Session) -> None:
    site = create_random_site(db)
    site_2 = create_random_site(db)
    stored_site = crud_site.site.get_multi(db)
    assert stored_site
    assert site in stored_site
    assert site_2 in stored_site


def test_search_site_by_name(db: Session) -> None:
    site = create_random_site(db)
    stored_site = crud_site.site.search_by_name(db, name=site.name)
    assert stored_site
    assert site in stored_site
