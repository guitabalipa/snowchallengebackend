from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class SiteImage(Base):
    __tablename__ = "site_images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    user_created_id = Column(Integer, ForeignKey("users.id"))
