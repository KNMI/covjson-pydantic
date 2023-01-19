import math
from enum import Enum
from typing import List
from typing import Literal
from typing import Optional

from pydantic import AnyUrl
from pydantic.class_validators import root_validator

from .base_models import BaseModel
from .base_models import CovJsonBaseModel


# TODO: Support for integers and strings
class DataType(str, Enum):
    float = "float"


class NdArray(CovJsonBaseModel):
    type: Literal["NdArray"] = "NdArray"
    dataType: DataType = DataType.float  # noqa: N815
    axisNames: Optional[List[str]]  # noqa: N815
    shape: Optional[List[int]]
    values: List[Optional[float]]

    @root_validator(skip_on_failure=True)
    def check_field_dependencies(cls, values):
        if len(values["values"]) > 1 and (values.get("axisNames") is None or len(values.get("axisNames")) == 0):
            raise ValueError("'axisNames' must to be provided if array is not 0D")

        if len(values["values"]) > 1 and (values.get("shape") is None or len(values.get("shape")) == 0):
            raise ValueError("'shape' must to be provided if array is not 0D")

        if (
            values.get("axisNames") is not None
            and values.get("shape") is not None
            and len(values.get("axisNames")) != len(values.get("shape"))
        ):
            raise ValueError("'axisNames' and 'shape' should have equal length")

        if values.get("shape") is not None and len(values.get("shape")) >= 1:
            prod = math.prod(values["shape"])
            if len(values["values"]) != prod:
                raise ValueError(
                    "Where 'shape' is present and non-empty, the product of its values MUST equal "
                    "the number of elements in the 'values' array."
                )

        return values


class TileSet(BaseModel):
    tileShape: List[Optional[int]]  # noqa: N815
    urlTemplate: AnyUrl  # noqa: N815


# TODO: Validation of field dependencies
class TiledNdArray(CovJsonBaseModel):
    type: Literal["TiledNdArray"] = "TiledNdArray"
    dataType: DataType = DataType.float  # noqa: N815
    axisNames: List[str]  # noqa: N815
    shape: List[int]
    tileSets: List[TileSet]  # noqa: N815
