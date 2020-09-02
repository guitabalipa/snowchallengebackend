from sqlalchemy.orm import Session

from app.schemas.favorite import FavoriteCreate

from app.crud import crud_favorite
from app.tests.utils.site import create_random_site
from app.tests.utils.user import create_random_user


def test_create_favorite(db: Session) -> None:
    user = create_random_user(db)
    site = create_random_site(db)
    favorite_in = FavoriteCreate(site_id=site.id)
    favorite = crud_favorite.favorite.create_favorite(db, obj_in=favorite_in, user_id=user.id)
    assert favorite.site_id == site.id
    assert favorite.user_id == user.id


def test_get_all_favorite_by_user(db: Session) -> None:
    user = create_random_user(db)
    site = create_random_site(db)
    site_2 = create_random_site(db)
    favorite_in = FavoriteCreate(site_id=site.id)
    favorite = crud_favorite.favorite.create_favorite(db, obj_in=favorite_in, user_id=user.id)
    favorite_in_2 = FavoriteCreate(site_id=site_2.id)
    favorite_2 = crud_favorite.favorite.create_favorite(db, obj_in=favorite_in_2, user_id=user.id)
    favorites = crud_favorite.favorite.get_all_by_user_id(db, user_id=user.id)
    assert favorites
    assert favorite in favorites
    assert favorite_2 in favorites


def test_delete_favorite(db: Session) -> None:
    user = create_random_user(db)
    site = create_random_site(db)
    favorite_in = FavoriteCreate(site_id=site.id)
    favorite = crud_favorite.favorite.create_favorite(db, obj_in=favorite_in, user_id=user.id)
    favorite_2 = crud_favorite.favorite.delete(db, user_id=favorite.user_id, site_id=favorite.site_id)
    favorite_3 = crud_favorite.favorite.find_favorite(db, user_id=user.id, site_id=site.id)
    assert favorite_3 is None
    assert favorite_2.user_id == favorite.user_id
    assert favorite_2.site_id == favorite.site_id
