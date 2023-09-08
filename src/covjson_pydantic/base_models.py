from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
    )


class CovJsonBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")
