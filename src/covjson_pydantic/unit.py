from typing import Optional
from typing import Union

from pydantic import model_validator

from .base_models import CovJsonBaseModel
from .i18n import i18n


class Symbol(CovJsonBaseModel):
    value: str
    type: str


class Unit(CovJsonBaseModel):
    id: Optional[str] = None
    label: Optional[i18n] = None
    symbol: Optional[Union[str, Symbol]] = None

    @model_validator(mode="after")
    def check_either_label_or_symbol(self):
        if self.label is None and self.symbol is None:
            raise ValueError("Either 'label' or 'symbol' should be set")

        return self
