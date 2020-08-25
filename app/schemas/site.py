from typing import List
from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.site_image import SiteImage


class SiteBase(BaseModel):
    name: str
    lat: str
    lon: str


class SiteCreate(SiteBase):
    category_id: int
    pass


class SiteUpdate(SiteBase):
    pass


class Site(SiteBase):
    id: int
    category: Category
    images: List[SiteImage] = []

    class Config:
        orm_mode = True
