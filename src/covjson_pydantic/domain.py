from datetime import datetime
from enum import Enum
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from pydantic import Extra
from pydantic import PositiveInt
from pydantic.class_validators import root_validator
from pydantic.generics import GenericModel

from .base_models import BaseModel
from .base_models import CovJsonBaseModel
from .reference_system import ReferenceSystemConnectionObject


class CompactAxis(BaseModel):
    start: float
    stop: float
    num: PositiveInt

    @root_validator(skip_on_failure=True)
    def single_value_case(cls, values):
        if values["num"] == 1 and values["start"] != values["stop"]:
            raise ValueError("If the value of 'num' is 1, then 'start' and 'stop' MUST have identical values.")
        return values


ValuesT = TypeVar("ValuesT")


class ValuesAxis(GenericModel, Generic[ValuesT]):
    dataType: Optional[str]  # noqa: N815
    coordinates: Optional[List[str]]
    values: List[ValuesT]
    bounds: Optional[List[ValuesT]]

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        extra = Extra.allow  # allow custom members
        validate_all = True
        validate_assignment = True

    @root_validator(skip_on_failure=True)
    def bounds_length(cls, values):
        if values["bounds"] is not None and len(values["bounds"]) != 2 * len(values["values"]):
            raise ValueError("If provided, the length of 'bounds' should be twice that of 'values'.")
        return values


class DomainType(str, Enum):
    grid = "Grid"
    vertical_profile = "VerticalProfile"
    point_series = "PointSeries"
    point = "Point"
    multi_point_series = "MultiPointSeries"
    multi_point = "MultiPoint"


class Axes(BaseModel):
    x: Optional[Union[ValuesAxis[float], CompactAxis]]
    y: Optional[Union[ValuesAxis[float], CompactAxis]]
    z: Optional[Union[ValuesAxis[float], CompactAxis]]
    t: Optional[ValuesAxis[datetime]]
    composite: Optional[ValuesAxis[Tuple]]

    @root_validator(skip_on_failure=True)
    def at_least_one_axes(cls, values):
        if (
            values["x"] is None
            and values["y"] is None
            and values["z"] is None
            and values["t"] is None
            and values["composite"] is None
        ):
            raise ValueError("At least one axis of x,y,z,t or composite must be given.")
        return values


class Domain(CovJsonBaseModel):
    type: Literal["Domain"] = "Domain"
    domainType: Optional[DomainType]  # noqa: N815
    axes: Axes
    referencing: Optional[List[ReferenceSystemConnectionObject]]

    @staticmethod
    def check_axis(domain_type, axes, required_axes, allowed_axes, single_value_axes):
        # Check required axes
        for axis_name in required_axes:
            axis = getattr(axes, axis_name)
            if axis is None:
                raise ValueError(f"A {domain_type} must have a '{axis_name}'-axis.")
            if axis_name in single_value_axes:
                if not (isinstance(axis, ValuesAxis) and len(axis.values) == 1):
                    raise ValueError(
                        f"The 'values' field of the '{axis_name}'-axis "
                        f"of a '{domain_type}' domain must contain a single value."
                    )

        # Check allowed axes
        all_axis = {"x", "y", "z", "t", "composite"}
        for axis_name in all_axis - required_axes - allowed_axes:
            axis = getattr(axes, axis_name)
            if axis is not None:
                raise ValueError(f"A {domain_type} domain can not have a '{axis_name}'-axis.")

        # Check for single value of allowed axes
        for axis_name in allowed_axes:
            axis = getattr(axes, axis_name)
            if axis is not None and axis_name in single_value_axes:
                if not (isinstance(axis, ValuesAxis) and len(axis.values) == 1):
                    raise ValueError(
                        f"If provided, the 'values' field of the '{axis_name}'-axis "
                        f"of a '{domain_type}' domain must contain a single value."
                    )

    @root_validator(skip_on_failure=True)
    def check_domain_consistent(cls, values):
        domain_type = values.get("domainType")
        axes = values.get("axes")

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

        return values
