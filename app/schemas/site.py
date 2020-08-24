from pydantic import BaseModel

from app.schemas.category import Category


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

    class Config:
        orm_mode = True
