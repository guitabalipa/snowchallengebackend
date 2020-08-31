from app.crud.base import CRUDBase
from app.models.site_picture import SitePicture
from app.schemas.site_picture import SitePictureCreate, SitePictureUpdate

from sqlalchemy.orm import Session


class CRUDSitePicture(CRUDBase[SitePicture, SitePictureCreate, SitePictureUpdate]):
    def create_site_picture(self, db: Session, obj_in: SitePictureCreate):
        db_obj = SitePicture(**obj_in)
        db.add(db_obj)
        return db_obj

    def delete_picture(self, db: Session, id_pic: int):
        obj = db.query(self.model).get(id_pic)
        db.delete(obj)
        return obj


site_picture = CRUDSitePicture(SitePicture)
