from typing import Dict
from typing import List
from typing import Literal
from typing import Union

from pydantic import model_validator

from .base_models import CovJsonBaseModel
from .base_models import OptionalS
from .i18n import i18n
from .observed_property import ObservedProperty
from .unit import Unit


class Parameter(CovJsonBaseModel, extra="allow"):
    type: Literal["Parameter"] = "Parameter"
    id: OptionalS[str] = None
    label: OptionalS[i18n] = None
    description: OptionalS[i18n] = None
    observedProperty: ObservedProperty  # noqa: N815
    categoryEncoding: OptionalS[Dict[str, Union[int, List[int]]]] = None  # noqa: N815
    unit: OptionalS[Unit] = None

    @model_validator(mode="after")
    def must_not_have_unit_if_observed_property_has_categories(self):
        if self.unit is not None and self.observedProperty is not None and self.observedProperty.categories is not None:
            raise ValueError(
                "A parameter object MUST NOT have a 'unit' member "
                "if the 'observedProperty' member has a 'categories' member."
            )

        return self


class ParameterGroup(CovJsonBaseModel, extra="allow"):
    type: Literal["ParameterGroup"] = "ParameterGroup"
    id: OptionalS[str] = None
    label: OptionalS[i18n] = None
    description: OptionalS[i18n] = None
    observedProperty: OptionalS[ObservedProperty] = None  # noqa: N815
    members: List[str]

    @model_validator(mode="after")
    def must_have_label_and_or_observed_property(self):
        if self.label is None and self.observedProperty is None:
            raise ValueError(
                "A parameter group object MUST have either or both the members 'label' or/and 'observedProperty'"
            )
        return self
