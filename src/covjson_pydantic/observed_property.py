from typing import List

from .base_models import CovJsonBaseModel
from .base_models import OptionalS
from .i18n import i18n


class Category(CovJsonBaseModel):
    id: str
    label: i18n
    description: OptionalS[i18n] = None


class ObservedProperty(CovJsonBaseModel):
    id: OptionalS[str] = None
    label: i18n
    description: OptionalS[i18n] = None
    categories: OptionalS[List[Category]] = None
