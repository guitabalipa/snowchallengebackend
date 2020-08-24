from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from app.schemas.favorite import Favorite, FavoriteCreate
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.site import Site
from app.crud import crud_user, crud_favorite, crud_site
from app.models import user as user_model
from app.api import deps

router = APIRouter()


@router.post("/", response_model=User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
) -> Any:
    user = crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return crud_user.user.create(db, obj_in=user_in)


@router.put("/me", response_model=User)
def update(
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        name: str = Body(None),
        email: str = Body(None),
        current_user: user_model.User = Depends(deps.get_current_active_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user.as_dict())
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if name is not None:
        user_in.name = name
    if email is not None:
        user_in.email = email
    user = crud_user.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user


@router.post("/me/favorites", response_model=Favorite)
def create_favorite(
        favorite_in: FavoriteCreate,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
):
    favorite = crud_favorite.favorite.find_favorite(
        db=db, user_id=current_user.id, site_id=favorite_in.site_id)
    if favorite:
        raise HTTPException(
            status_code=400,
            detail="Favorite already created.",
        )

    site = crud_site.site.get(db=db, id=favorite_in.site_id)
    if not site:
        raise HTTPException(
            status_code=400,
            detail="Site not found.",
        )

    return crud_favorite.favorite.create_favorite(db=db, fav_create=favorite_in, user_id=current_user.id)


@router.get("/me/favorites", response_model=List[Site])
def read_favorite(current_user: user_model.User = Depends(deps.get_current_active_user)):
    return current_user.site_favorites


@router.delete("/me/favorites")
def delete_favorite(
        site_id: int,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)):
    return crud_favorite.favorite.delete(db=db, user_id=current_user.id, site_id=site_id)
