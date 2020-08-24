from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteUpdate

from sqlalchemy.orm import Session


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteUpdate]):
    def get_all_by_user_id(self, db: Session, user_id: int):
        return db.query(Favorite).filter(Favorite.user_id == user_id).all()

    def find_favorite(self, db: Session, user_id: int, site_id: int):
        return db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.site_id == site_id).first()

    def create_favorite(self, db: Session, fav_create: FavoriteCreate, user_id: int):
        db_fav = Favorite(**fav_create.dict(), user_id=user_id)
        db.add(db_fav)
        db.commit()
        db.refresh(db_fav)
        return db_fav

    def delete(self, db:Session, user_id: int, site_id: int):
        db_fav = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.site_id == site_id).first()
        db.delete(db_fav)
        db.commit()


favorite = CRUDFavorite(Favorite)
