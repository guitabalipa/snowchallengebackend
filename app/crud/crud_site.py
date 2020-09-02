from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate


class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):
    def get_by_name(self, db: Session, name: str):
        return db.query(Site).filter(Site.name.ilike(name)).first()

    def search_by_name(self, db: Session, name: str):
        return db.query(Site).filter(Site.name.ilike("%" + name + "%")).all()


site = CRUDSite(Site)
