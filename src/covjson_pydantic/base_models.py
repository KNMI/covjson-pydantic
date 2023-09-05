import orjson
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


def orjson_dumps(v, *, default, indent=None, sort_keys=False):
    options = orjson.OPT_NON_STR_KEYS | orjson.OPT_UTC_Z | orjson.OPT_NAIVE_UTC
    if indent:
        options |= orjson.OPT_INDENT_2

    if sort_keys:
        options |= orjson.OPT_SORT_KEYS

    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, option=options).decode()


class BaseModel(PydanticBaseModel):
    # TODO[pydantic]: The following keys were removed: `json_loads`, `json_dumps`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
        json_loads=orjson.loads,
        json_dumps=orjson_dumps,
    )


class CovJsonBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")
