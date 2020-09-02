from sqlalchemy.orm import Session

from app.tests.utils.utils import random_picture_name
from app.schemas.site_picture import SitePictureCreate
from app.crud import crud_site_picture
from app.tests.utils.site import create_random_site
from app.tests.utils.user import create_random_user


def test_create_site_picture(db: Session) -> None:
    user = create_random_user(db)
    site = create_random_site(db)
    name = random_picture_name()
    picture_in = SitePictureCreate(name=name, site_id=site.id, user_created_id=user.id)
    picture = crud_site_picture.site_picture.create_site_picture(db, obj_in=picture_in)
    db.commit()
    assert picture.name == name
    assert picture.user_created_id == user.id
    assert picture.site_id == site.id


def test_delete_site_picture(db: Session) -> None:
    user = create_random_user(db)
    site = create_random_site(db)
    name = random_picture_name()
    picture_in = SitePictureCreate(name=name, site_id=site.id, user_created_id=user.id)
    picture = crud_site_picture.site_picture.create(db, obj_in=picture_in)
    picture_2 = crud_site_picture.site_picture.delete_picture(db, id=picture.id)
    db.commit()
    picture_3 = crud_site_picture.site_picture.get(db, id=picture.id)
    assert picture_3 is None
    assert picture_2.id == picture.id
    assert picture_2.name == picture.name
    assert picture_2.site_id == picture.site_id
    assert picture_2.user_created_id == picture.user_created_id
