from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import AnyUrl
from pydantic import model_validator

from .base_models import CovJsonBaseModel
from .i18n import i18n


class TargetConcept(CovJsonBaseModel):
    id: Optional[str] = None  # Not in spec, but needed for example in spec for 'Identifier-based Reference Systems'
    label: i18n
    description: Optional[i18n] = None


class ReferenceSystem(CovJsonBaseModel, extra="allow"):
    type: Literal["GeographicCRS", "ProjectedCRS", "VerticalCRS", "TemporalRS", "IdentifierRS"]
    id: Optional[str] = None
    description: Optional[i18n] = None

    # Only for TemporalRS
    calendar: Optional[Union[Literal["Gregorian"], AnyUrl]] = None
    timeScale: Optional[AnyUrl] = None  # noqa: N815

    # Only for IdentifierRS
    label: Optional[i18n] = None
    targetConcept: Optional[TargetConcept] = None  # noqa: N815
    identifiers: Optional[Dict[str, TargetConcept]] = None

    @model_validator(mode="after")
    def check_type_specific_fields(self):
        if self.type != "TemporalRS" and (self.calendar is not None or self.timeScale is not None):
            raise ValueError("'calendar' and 'timeScale' fields can only be used for type 'TemporalRS'")

        if self.type != "IdentifierRS" and (
            self.label is not None or self.targetConcept is not None or self.identifiers is not None
        ):
            raise ValueError(
                "'label', 'targetConcept' and 'identifiers' fields can only be used for type 'IdentifierRS'"
            )

        if self.type == "IdentifierRS" and self.targetConcept is None:
            raise ValueError("An identifier RS object MUST have a member 'targetConcept'")

        return self


class ReferenceSystemConnectionObject(CovJsonBaseModel):
    coordinates: List[str]
    system: ReferenceSystem
