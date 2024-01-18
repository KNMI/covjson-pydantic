from typing import Annotated
from typing import TypeVar
from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema


# Define an alternative Optional type that doesn't show the None/null value and the default in the schema
T = TypeVar("T")
OptionalS = Annotated[Union[T, SkipJsonSchema[None]], Field(json_schema_extra=lambda x: x.pop("default"))]


class CovJsonBaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
        strict=True,
    )
