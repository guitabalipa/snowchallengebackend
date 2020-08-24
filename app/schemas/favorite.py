from pydantic import BaseModel


class FavoriteBase(BaseModel):
    site_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteUpdate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    user_id: int

    class Config:
        orm_mode = True
