from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import AnyUrl
from pydantic import Extra
from pydantic.class_validators import root_validator

from .base_models import BaseModel
from .i18n import i18n


class TargetConcept(BaseModel):
    id: Optional[str]  # Not in spec, but needed for example in spec for 'Identifier-based Reference Systems'
    label: i18n
    description: Optional[i18n]


class ReferenceSystem(BaseModel, extra=Extra.allow):
    type: Literal["GeographicCRS", "ProjectedCRS", "VerticalCRS", "TemporalRS", "IdentifierRS"]
    id: Optional[str]
    description: Optional[i18n]

    # Only for TemporalRS
    calendar: Optional[Union[Literal["Gregorian"], AnyUrl]]
    timeScale: Optional[AnyUrl]  # noqa: N815

    # Only for IdentifierRS
    label: Optional[i18n]
    targetConcept: Optional[TargetConcept]  # noqa: N815
    identifiers: Optional[Dict[str, TargetConcept]]

    @root_validator(skip_on_failure=True)
    def check_type_specific_fields(cls, values):
        if values["type"] != "TemporalRS" and (
            values.get("calendar") is not None or values.get("timeScale") is not None
        ):
            raise ValueError("'calendar' and 'timeScale' fields can only be used for type 'TemporalRS'")

        if values["type"] != "IdentifierRS" and (
            values.get("label") is not None
            or values.get("targetConcept") is not None
            or values.get("identifiers") is not None
        ):
            raise ValueError(
                "'label', 'targetConcept' and 'identifiers' fields can only be used for type 'IdentifierRS'"
            )

        if values["type"] == "IdentifierRS" and values.get("targetConcept") is None:
            raise ValueError("An identifier RS object MUST have a member 'targetConcept'")

        return values


class ReferenceSystemConnectionObject(BaseModel):
    coordinates: List[str]
    system: ReferenceSystem
