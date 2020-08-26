from app.services.storage.s3 import upload_file_to_s3

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.schemas.site import Site, SiteCreate, SiteUpdate
from app.schemas.site_picture import SitePicture, SitePictureCreate
from app.crud import crud_site
from app.crud import crud_site_picture
from app.models import user as user_model
from app.api import deps

router = APIRouter()


@router.post("/form/", response_model=Site)
def create_form(
        name: str = Form(...),
        latitude: str = Form(...),
        longitude: str = Form(...),
        category_id: int = Form(...),
        pictures: List[UploadFile] = File(...),
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

    for picture in pictures:
        filename = upload_file_to_s3(picture, picture.content_type.split("/")[1])
        crud_site_picture.site_picture.create(
            db=db,
            obj_in=SitePictureCreate(name=filename, site_id=db_obj.id, user_created_id=current_user.id)
        )

    return db_obj


@router.put("/{site_id}/", response_model=Site)
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


@router.post("/{site_id}/picture/")
def upload_pictures(
        site_id: int,
        pictures: List[UploadFile] = File(...),
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)):
    site = crud_site.site.get(db=db, id=site_id)

    if not site:
        raise HTTPException(
            status_code=404,
            detail="A Site with this ID does not exist in the system",
        )

    for picture in pictures:
        filename = upload_file_to_s3(picture, picture.content_type.split("/")[1])
        crud_site_picture.site_picture.create(
            db=db,
            obj_in=SitePictureCreate(name=filename, site_id=site_id, user_created_id=current_user.id)
        )


@router.delete("/{site_id}/picture/{picture_id}/", response_model=SitePicture)
def delete_picture(site_id: int, picture_id: int,
                   db: Session = Depends(deps.get_db),
                   current_user: user_model.User = Depends(deps.get_current_active_user)):
    site = crud_site.site.get(db=db, id=site_id)
    if not site:
        raise HTTPException(
            status_code=404,
            detail="A Site with this ID does not exist in the system",
        )

    picture = crud_site_picture.site_picture.get(db=db, id=picture_id)
    if not picture:
        raise HTTPException(
            status_code=404,
            detail="A Picture with this ID does not exist in the system",
        )

    if picture.user_created_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="This user don't have permission to delete the picture!",
        )

    try:
        deleted_picture = crud_site_picture.site_picture.delete_picture(db=db, id_pic=picture_id)

        return deleted_picture
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to delete file",
        )
