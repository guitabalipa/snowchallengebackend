from app.services.storage.s3 import upload_image_s3

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.schemas.site import Site, SiteCreate, SiteUpdate
from app.schemas.site_image import SiteImageCreate
from app.crud import crud_site
from app.crud import crud_site_image
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


@router.post("/form/", response_model=Site)
def create_form(
        name: str = Form(...),
        latitude: str = Form(...),
        longitude: str = Form(...),
        category_id: int = Form(...),
        images: List[UploadFile] = File(...),
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
):
    category = crud_site.site.get_by_name(db=db, name=name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="A site with this exact name already exists in the system.",
        )

    form_in = SiteCreate(name=name, lat=latitude, lon=longitude, category_id=category_id)

    db_obj = crud_site.site.create(db=db, obj_in=form_in)

    for image in images:
        filename = upload_image_s3(image, image.content_type.split("/")[1])
        crud_site_image.site_image.create(db=db, obj_in=SiteImageCreate(name=filename, site_id=db_obj.id,
                                                                        user_created_id=current_user.id))

    return db_obj


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
def search_by_name(db: Session = Depends(deps.get_db), name: str = ""):
    return crud_site.site.search_by_name(db=db, name=name)


@router.post("/image/")
def upload_image(
        form: Optional[str] = Form(None),
        files: List[UploadFile] = File(...)):
    for file in files:
        upload_image_s3(file, "0101")

    return {
        "filenames": [file.filename for file in files],
        "form": form
    }
