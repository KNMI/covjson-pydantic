from typing import Optional
from typing import Union

from pydantic import model_validator
from pydantic.class_validators import root_validator

from .base_models import BaseModel
from .i18n import i18n


class Symbol(BaseModel):
    value: str
    type: str


class Unit(BaseModel):
    id: Optional[str] = None
    label: Optional[i18n] = None
    symbol: Optional[Union[str, Symbol]] = None

    @model_validator(skip_on_failure=True)
    @classmethod
    def check_either_label_or_symbol(cls, values):
        if values.get("label") is None and values.get("symbol") is None:
            raise ValueError("Either 'label' or 'symbol' should be set")

        return values
