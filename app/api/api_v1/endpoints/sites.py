import geopy.distance

from app.services.storage.s3 import upload_file_to_s3, create_pre_signed_url, delete_file_from_s3

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.schemas.site import Site, SiteCreate, SiteUpdate, SiteOut
from app.schemas.site_picture import SitePicture, SitePictureCreate
from app.crud import crud_site
from app.crud import crud_site_picture
from app.models import user as user_model
from app.api import deps

router = APIRouter()


@router.post("/", response_model=Site)
def create(
        site_in: SiteCreate,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
):
    site = crud_site.site.get_by_name(db=db, name=site_in.name)
    if site:
        raise HTTPException(
            status_code=400,
            detail="A site with this exact name already exists in the system.",
        )

    try:
        return crud_site.site.create(db=db, obj_in=site_in)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Failed to create site!",
        )


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
    site_updated = crud_site.site.update(db, db_obj=site, obj_in=site_in)
    return map_site_pics(site_updated)


@router.get("/", response_model=List[Site])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    sites = crud_site.site.get_multi(db, skip=skip, limit=limit)
    mapped_sites = []
    for site in sites:
        mapped_sites.append(map_site_pics(site))

    return mapped_sites


@router.get("/name/", response_model=List[Site])
def search_by_name(db: Session = Depends(deps.get_db), name: str = ""):
    sites = crud_site.site.search_by_name(db=db, name=name)
    mapped_sites = []
    for site in sites:
        mapped_sites.append(map_site_pics(site))

    return mapped_sites


@router.get("/location/", response_model=List[Site])
def get_nearby_sites(lat: str, lon: str, db: Session = Depends(deps.get_db)):
    sites = crud_site.site.get_multi(db=db)

    nearby_sites = []
    for site in sites:
        coord1 = (lat, lon)
        coord2 = (site.lat, site.lon)

        try:
            dist = geopy.distance.distance(coord1, coord2).km
        except Exception:
            raise HTTPException(
                status_code=404,
                detail="Invalid Lat/Lon value!",
            )

        if dist < 5:
            nearby_sites.append(map_site_pics(site))

    return nearby_sites


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
        db_obj = crud_site_picture.site_picture.delete_picture(db=db, id=picture_id)
        delete_file_from_s3(db_obj.name)

        db.commit()

        return db_obj
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to delete image!",
        )


def map_site_pics(site: Site):
    pics = site.pictures
    urls_pics = []
    for pic in pics:
        urls_pics.append(SitePicture(id=pic.id, name=create_pre_signed_url(pic.name)))

    return Site(
        id=site.id,
        category=site.category,
        name=site.name,
        lat=site.lat,
        lon=site.lon,
        pictures=urls_pics
    )
