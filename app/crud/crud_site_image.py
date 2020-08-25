from app.crud.base import CRUDBase
from app.models.site_image import SiteImage
from app.schemas.site_image import SiteImageCreate, SiteImageUpdate

from sqlalchemy.orm import Session


class CRUDSiteImage(CRUDBase[SiteImage, SiteImageCreate, SiteImageUpdate]):
    def create_image(self, db: Session, create: SiteImageCreate):
        db_image = SiteImage(**create.dict())
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image


site_image = CRUDSiteImage(SiteImage)
