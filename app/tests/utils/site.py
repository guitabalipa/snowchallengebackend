from sqlalchemy.orm import Session

from app.tests.utils.utils import random_category_name, random_site_name

from app.crud import crud_category, crud_site
from app.schemas.category import CategoryCreate
from app.schemas.site import SiteCreate


def create_random_site(db: Session):
    cat_name = random_category_name()
    category_in = CategoryCreate(name=cat_name)
    category = crud_category.category.create(db, obj_in=category_in)

    name = random_site_name()
    lat = "78797979"
    lon = "76876868"

    site_in = SiteCreate(name=name, lat=lat, lon=lon, category_id=category.id)
    return crud_site.site.create(db, obj_in=site_in)
