from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import Extra
from pydantic.class_validators import root_validator

from .base_models import BaseModel
from .i18n import i18n
from .observed_property import ObservedProperty
from .unit import Unit


class Parameter(BaseModel, extra=Extra.allow):
    type: Literal["Parameter"] = "Parameter"
    id: Optional[str]
    label: Optional[i18n]
    description: Optional[i18n]
    observedProperty: ObservedProperty  # noqa: N815
    categoryEncoding: Optional[Dict[str, Union[int, List[int]]]]  # noqa: N815
    unit: Optional[Unit]

    @root_validator(skip_on_failure=True)
    def must_not_have_unit_if_observed_property_has_categories(cls, values):
        if (
            values.get("unit") is not None
            and values.get("observedProperty") is not None
            and values.get("observedProperty").categories is not None
        ):
            raise ValueError(
                "A parameter object MUST NOT have a 'unit' member "
                "if the 'observedProperty' member has a 'categories' member."
            )

        return values


class ParameterGroup(BaseModel, extra=Extra.allow):
    type: Literal["ParameterGroup"] = "ParameterGroup"
    id: Optional[str]
    label: Optional[i18n]
    description: Optional[i18n]
    observedProperty: Optional[ObservedProperty]  # noqa: N815
    members: List[str]

    @root_validator(skip_on_failure=True)
    def must_have_label_and_or_observed_property(cls, values):
        if values.get("label") is None and values.get("observedProperty") is None:
            raise ValueError(
                "A parameter group object MUST have either or both the members 'label' or/and 'observedProperty'"
            )
        return values
