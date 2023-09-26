from typing import List
from typing import Optional

from .base_models import CovJsonBaseModel
from .i18n import i18n


class Category(CovJsonBaseModel):
    id: str
    label: i18n
    description: Optional[i18n] = None


class ObservedProperty(CovJsonBaseModel):
    id: Optional[str] = None
    label: i18n
    description: Optional[i18n] = None
    categories: Optional[List[Category]] = None
