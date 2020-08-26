from pydantic import BaseModel


class SitePictureBase(BaseModel):
    name: str


class SitePictureCreate(SitePictureBase):
    site_id: int
    user_created_id: int
    pass


class SitePictureUpdate(SitePictureBase):
    pass


class SitePicture(SitePictureBase):
    id: int

    class Config:
        orm_mode = True
