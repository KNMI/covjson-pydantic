# from typing import Annotated
import typing
from typing import TypeVar
from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


# Define an alternative Optional type that doesn't show the None/null value and the default in the schema
T = TypeVar("T")
if hasattr(typing, "Annotated"):  # Check if Annotated exists (Python >=3.9)
    OptionalS = typing.Annotated[Union[T, SkipJsonSchema[None]], Field(json_schema_extra=lambda x: x.pop("default"))]
else:  # For Python 3.8 we don't support dropping the default value
    OptionalS = Union[T, SkipJsonSchema[None]]  # type: ignore


class CovJsonBaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
        strict=True,
    )
