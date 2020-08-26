from app.crud.base import CRUDBase
from app.models.site_picture import SitePicture
from app.schemas.site_picture import SitePictureCreate, SitePictureUpdate

from sqlalchemy.orm import Session

from app.services.storage.s3 import delete_file_from_s3


class CRUDSitePicture(CRUDBase[SitePicture, SitePictureCreate, SitePictureUpdate]):
    def delete_picture(self, db: Session, id_pic: int):
        obj = db.query(self.model).get(id_pic)
        db.delete(obj)

        # TODO: discuss a better alternative to this
        try:
            delete_file_from_s3(obj.name)
        except Exception as e:
            db.rollback()
            return e

        db.commit()
        return obj


site_picture = CRUDSitePicture(SitePicture)
