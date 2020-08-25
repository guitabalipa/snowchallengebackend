from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.site_image import SiteImage
from app.models.category import Category


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lat = Column(String, index=True)
    lon = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship(Category)
    images = relationship(SiteImage)
