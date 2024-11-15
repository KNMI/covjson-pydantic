import math
from typing import List
from typing import Literal
from typing import Optional

from pydantic import model_validator

from .base_models import CovJsonBaseModel


class NdArray(CovJsonBaseModel, extra="allow"):
    type: Literal["NdArray"] = "NdArray"
    dataType: str  # Kept here to ensure order of output in JSON  # noqa: N815
    axisNames: Optional[List[str]] = None  # noqa: N815
    shape: Optional[List[int]] = None

    def __new__(cls, *args, **kwargs):
        if cls is NdArray:
            raise TypeError(
                "NdArray cannot be instantiated directly, please use a NdArrayFloat, NdArrayInt or NdArrayStr"
            )
        return super().__new__(cls)

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


class NdArrayFloat(NdArray):
    dataType: Literal["float"] = "float"  # noqa: N815
    values: List[Optional[float]]


class NdArrayInt(NdArray):
    dataType: Literal["integer"] = "integer"  # noqa: N815
    values: List[Optional[int]]


class NdArrayStr(NdArray):
    dataType: Literal["string"] = "string"  # noqa: N815
    values: List[Optional[str]]


class TileSet(CovJsonBaseModel):
    tileShape: List[Optional[int]]  # noqa: N815
    urlTemplate: str  # noqa: N815


# TODO: Validation of field dependencies
class TiledNdArray(CovJsonBaseModel, extra="allow"):
    type: Literal["TiledNdArray"] = "TiledNdArray"
    dataType: Literal["float"] = "float"  # noqa: N815
    axisNames: List[str]  # noqa: N815
    shape: List[int]
    tileSets: List[TileSet]  # noqa: N815
