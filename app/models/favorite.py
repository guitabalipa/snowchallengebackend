from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class Favorite(Base):
    __tablename__ = "favorites"

    site_id = Column(Integer, ForeignKey("sites.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

