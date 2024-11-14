import math
import typing
from enum import Enum
from typing import List
from typing import Literal
from typing import Optional

from pydantic import model_validator
from typing_extensions import Generic
from typing_extensions import TypeVar

from .base_models import CovJsonBaseModel


class DataType(str, Enum):
    float = "float"
    str = "string"
    int = "integer"


NdArrayTypeT = TypeVar("NdArrayTypeT")


class NdArray(CovJsonBaseModel, Generic[NdArrayTypeT], extra="allow"):
    type: Literal["NdArray"] = "NdArray"
    dataType: DataType = None  # noqa: N815
    axisNames: Optional[List[str]] = None  # noqa: N815
    shape: Optional[List[int]] = None
    values: List[Optional[NdArrayTypeT]] = []

    @model_validator(mode="before")
    @classmethod
    def set_data_type(cls, v):
        if type(v) is not dict:
            return v

        if "dataType" in v:
            v["dataType"] = DataType(v["dataType"])
            return v

        t = typing.get_args(cls.model_fields["values"].annotation)[0]
        if t == typing.Optional[float]:
            v["dataType"] = DataType.float
        elif t == typing.Optional[int]:
            v["dataType"] = DataType.int
        elif t == typing.Optional[str]:
            v["dataType"] = DataType.str
        else:
            raise ValueError(f"Unsupported NdArray type: {t}")
        return v

    @model_validator(mode="after")
    def check_data_type(self):
        t = typing.get_args(self.model_fields["values"].annotation)[0]
        if t == typing.Optional[NdArrayTypeT]:
            given_type = self.dataType.name if isinstance(self.dataType, DataType) else ""
            raise ValueError(f"No NdArray type given, please specify as NdArray[{given_type}]")
        if self.dataType == DataType.float and not t == typing.Optional[float]:
            raise ValueError("dataType and NdArray type must both be float.")
        if self.dataType == DataType.str and not t == typing.Optional[str]:
            raise ValueError("dataType and NdArray type must both be string.")
        if self.dataType == DataType.int and not t == typing.Optional[int]:
            raise ValueError("dataType and NdArray type must both be integer.")

        return self

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
