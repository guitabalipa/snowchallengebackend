# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.category import Category  # noqa
from app.models.site_picture import SitePicture  # noqa
from app.models.user import User  # noqa
from app.models.site import Site  # noqa
from app.models.favorite import Favorite  # noqa
