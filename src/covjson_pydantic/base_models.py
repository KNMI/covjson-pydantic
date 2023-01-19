import orjson
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(
        v, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_UTC_Z | orjson.OPT_NAIVE_UTC
    ).decode()


class BaseModel(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        extra = Extra.forbid
        validate_all = True
        validate_assignment = True

        json_loads = orjson.loads
        json_dumps = orjson_dumps


class CovJsonBaseModel(BaseModel):
    class Config:
        extra = Extra.allow  # allow custom members
