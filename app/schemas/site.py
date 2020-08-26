from typing import List
from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.site_picture import SitePicture


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
    pictures: List[SitePicture] = []

    class Config:
        orm_mode = True


class SiteOut(BaseModel):
    id: int
    category: Category
    name: str
    lat: str
    lon: str
    pictures: List[str] = []
