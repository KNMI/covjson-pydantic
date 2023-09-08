from enum import Enum
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from pydantic import AwareDatetime
from pydantic import ConfigDict
from pydantic import model_validator
from pydantic import PositiveInt

from .base_models import BaseModel
from .base_models import CovJsonBaseModel
from .reference_system import ReferenceSystemConnectionObject


class CompactAxis(BaseModel):
    start: float
    stop: float
    num: PositiveInt

    @model_validator(mode="after")
    def single_value_case(self):
        if self.num == 1 and self.start != self.stop:
            raise ValueError("If the value of 'num' is 1, then 'start' and 'stop' MUST have identical values.")
        return self


ValuesT = TypeVar("ValuesT")


class ValuesAxis(BaseModel, Generic[ValuesT]):
    dataType: Optional[str] = None  # noqa: N815
    coordinates: Optional[List[str]] = None
    values: List[ValuesT]
    bounds: Optional[List[ValuesT]] = None
    model_config = ConfigDict(
        str_strip_whitespace=True, str_min_length=1, extra="allow", validate_default=True, validate_assignment=True
    )

    @model_validator(mode="after")
    def bounds_length(self):
        if self.bounds is not None and len(self.bounds) != 2 * len(self.values):
            raise ValueError("If provided, the length of 'bounds' should be twice that of 'values'.")
        return self


class DomainType(str, Enum):
    grid = "Grid"
    vertical_profile = "VerticalProfile"
    point_series = "PointSeries"
    point = "Point"
    multi_point_series = "MultiPointSeries"
    multi_point = "MultiPoint"


class Axes(BaseModel):
    x: Optional[Union[ValuesAxis[float], CompactAxis]] = None
    y: Optional[Union[ValuesAxis[float], CompactAxis]] = None
    z: Optional[Union[ValuesAxis[float], CompactAxis]] = None
    t: Optional[ValuesAxis[AwareDatetime]] = None
    composite: Optional[ValuesAxis[Tuple]] = None

    @model_validator(mode="after")
    def at_least_one_axes(self):
        if self.x is None and self.y is None and self.z is None and self.t is None and self.composite is None:
            raise ValueError("At least one axis of x,y,z,t or composite must be given.")
        return self


class Domain(CovJsonBaseModel):
    type: Literal["Domain"] = "Domain"
    domainType: Optional[DomainType] = None  # noqa: N815
    axes: Axes
    referencing: Optional[List[ReferenceSystemConnectionObject]] = None

    @staticmethod
    def check_axis(domain_type, axes, required_axes, allowed_axes, single_value_axes):
        # Check required axes
        for axis_name in required_axes:
            axis = getattr(axes, axis_name)
            if axis is None:
                raise ValueError(f"A '{domain_type.value}' must have a '{axis_name}'-axis.")
            if axis_name in single_value_axes:
                if not (isinstance(axis, ValuesAxis) and len(axis.values) == 1):
                    raise ValueError(
                        f"The 'values' field of the '{axis_name}'-axis "
                        f"of a '{domain_type.value}' domain must contain a single value."
                    )

        # Check allowed axes
        all_axis = {"x", "y", "z", "t", "composite"}
        for axis_name in all_axis - required_axes - allowed_axes:
            axis = getattr(axes, axis_name)
            if axis is not None:
                raise ValueError(f"A '{domain_type.value}' domain can not have a '{axis_name}'-axis.")

        # Check for single value of allowed axes
        for axis_name in allowed_axes:
            axis = getattr(axes, axis_name)
            if axis is not None and axis_name in single_value_axes:
                if not (isinstance(axis, ValuesAxis) and len(axis.values) == 1):
                    raise ValueError(
                        f"If provided, the 'values' field of the '{axis_name}'-axis "
                        f"of a '{domain_type.value}' domain must contain a single value."
                    )

    @model_validator(mode="after")
    def check_domain_consistent(self):
        domain_type = self.domainType
        axes = self.axes

        if domain_type == DomainType.grid:
            Domain.check_axis(
                domain_type, axes, required_axes={"x", "y"}, allowed_axes={"z", "t"}, single_value_axes=set()
            )

        if domain_type == DomainType.vertical_profile:
            Domain.check_axis(
                domain_type, axes, required_axes={"x", "y", "z"}, allowed_axes={"t"}, single_value_axes={"x", "y", "t"}
            )

        if domain_type == DomainType.point_series:
            Domain.check_axis(
                domain_type, axes, required_axes={"x", "y", "t"}, allowed_axes={"z"}, single_value_axes={"x", "y", "z"}
            )

        if domain_type == DomainType.point:
            Domain.check_axis(
                domain_type,
                axes,
                required_axes={"x", "y"},
                allowed_axes={"z", "t"},
                single_value_axes={"x", "y", "z", "t"},
            )

        if domain_type == DomainType.multi_point_series:
            Domain.check_axis(
                domain_type, axes, required_axes={"composite", "t"}, allowed_axes=set(), single_value_axes=set()
            )

        if domain_type == DomainType.multi_point:
            Domain.check_axis(
                domain_type, axes, required_axes={"composite"}, allowed_axes={"t"}, single_value_axes={"t"}
            )

        return self
