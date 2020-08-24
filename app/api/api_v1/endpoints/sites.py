from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.site import Site, SiteCreate, SiteUpdate
from app.crud import crud_site
from app.models import user as user_model
from app.api import deps

router = APIRouter()


@router.post("/", response_model=Site)
def create(
        form_in: SiteCreate,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
):
    category = crud_site.site.get_by_name(db=db, name=form_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="A site with this exact name already exists in the system.",
        )
    return crud_site.site.create(db=db, obj_in=form_in)


@router.put("/{site_id}", response_model=Site)
def update(
        site_id: int,
        site_in: SiteUpdate,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
) -> Any:
    site = crud_site.site.get(db=db, id=site_id)
    if not site:
        raise HTTPException(
            status_code=404,
            detail="This site does not exist in the system",
        )
    user = crud_site.site.update(db, db_obj=site, obj_in=site_in)
    return user


@router.get("/", response_model=List[Site])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_site.site.get_multi(db, skip=skip, limit=limit)


@router.get("/name/", response_model=List[Site])
async def search_by_name(db: Session = Depends(deps.get_db), name: str = ""):
    return crud_site.site.search_by_name(db=db, name=name)
