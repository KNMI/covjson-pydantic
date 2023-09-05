from typing import List
from typing import Optional

from .base_models import BaseModel
from .i18n import i18n


class Category(BaseModel):
    id: str
    label: i18n
    description: Optional[i18n] = None


class ObservedProperty(BaseModel):
    id: Optional[str] = None
    label: i18n
    description: Optional[i18n] = None
    categories: Optional[List[Category]] = None
