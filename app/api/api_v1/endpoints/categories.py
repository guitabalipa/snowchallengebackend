from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.category import Category, CategoryCreate
from app.crud import crud_category
from app.models import user as user_model
from app.api import deps

router = APIRouter()


@router.post("/", response_model=Category)
def create_category(
        category_in: CategoryCreate,
        db: Session = Depends(deps.get_db),
        current_user: user_model.User = Depends(deps.get_current_active_user)
):
    category = crud_category.category.get_by_name(db=db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="This category already exists in the system.",
        )
    return crud_category.category.create(db=db, obj_in=category_in)


@router.get("/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_category.category.get_multi(db, skip=skip, limit=limit)
