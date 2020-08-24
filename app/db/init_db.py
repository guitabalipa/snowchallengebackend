from sqlalchemy.orm import Session

from app.db.session import engine
from app.db.base import Base
from app.crud.crud_category import category
from app.schemas.category import CategoryCreate


def init_db(db: Session) -> None:
    # TODO
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    category.create(db=db, obj_in=CategoryCreate(name="Park"))
    category.create(db=db, obj_in=CategoryCreate(name="Museum"))
    category.create(db=db, obj_in=CategoryCreate(name="Theater"))
    category.create(db=db, obj_in=CategoryCreate(name="Monument"))
