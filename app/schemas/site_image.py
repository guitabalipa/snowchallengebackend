from pydantic import BaseModel


class SiteImageBase(BaseModel):
    name: str


class SiteImageCreate(SiteImageBase):
    site_id: int
    user_created_id: int
    pass


class SiteImageUpdate(SiteImageBase):
    pass


class SiteImage(SiteImageBase):
    id: int

    class Config:
        orm_mode = True
