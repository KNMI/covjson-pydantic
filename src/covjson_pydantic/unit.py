from typing import Optional
from typing import Union

from pydantic.class_validators import root_validator

from .base_models import BaseModel
from .i18n import i18n


class Symbol(BaseModel):
    value: str
    type: str


class Unit(BaseModel):
    id: Optional[str]
    label: Optional[i18n]
    symbol: Optional[Union[str, Symbol]]

    @root_validator(skip_on_failure=True)
    def check_either_label_or_symbol(cls, values):
        if values.get("label") is None and values.get("symbol") is None:
            raise ValueError("Either 'label' or 'symbol' should be set")

        return values
