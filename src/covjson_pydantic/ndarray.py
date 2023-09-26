import math
from enum import Enum
from typing import List
from typing import Literal
from typing import Optional

from pydantic import model_validator

from .base_models import CovJsonBaseModel


# TODO: Support for integers and strings
class DataType(str, Enum):
    float = "float"


class NdArray(CovJsonBaseModel, extra="allow"):
    type: Literal["NdArray"] = "NdArray"
    dataType: DataType = DataType.float  # noqa: N815
    axisNames: Optional[List[str]] = None  # noqa: N815
    shape: Optional[List[int]] = None
    values: List[Optional[float]]

    @model_validator(mode="after")
    def check_field_dependencies(self):
        if len(self.values) > 1 and (self.axisNames is None or len(self.axisNames) == 0):
            raise ValueError("'axisNames' must to be provided if array is not 0D")

        if len(self.values) > 1 and (self.shape is None or len(self.shape) == 0):
            raise ValueError("'shape' must to be provided if array is not 0D")

        if self.axisNames is not None and self.shape is not None and len(self.axisNames) != len(self.shape):
            raise ValueError("'axisNames' and 'shape' should have equal length")

        if self.shape is not None and len(self.shape) >= 1:
            prod = math.prod(self.shape)
            if len(self.values) != prod:
                raise ValueError(
                    "Where 'shape' is present and non-empty, the product of its values MUST equal "
                    "the number of elements in the 'values' array."
                )

        return self


class TileSet(CovJsonBaseModel):
    tileShape: List[Optional[int]]  # noqa: N815
    urlTemplate: str  # noqa: N815


# TODO: Validation of field dependencies
class TiledNdArray(CovJsonBaseModel, extra="allow"):
    type: Literal["TiledNdArray"] = "TiledNdArray"
    dataType: DataType = DataType.float  # noqa: N815
    axisNames: List[str]  # noqa: N815
    shape: List[int]
    tileSets: List[TileSet]  # noqa: N815
