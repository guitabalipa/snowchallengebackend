from typing import Optional, List

from app.schemas.site import Site
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    site_favorites: List[Site] = []

    class Config:
        orm_mode = True
