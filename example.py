import datetime
import json

from covjson_pydantic.coverage import Coverage
from covjson_pydantic.domain import Domain
from covjson_pydantic.ndarray import NdArray


def pretty_print_json(json_str):
    print(json.dumps(json.loads(json_str), indent=4))


c = Coverage(
    domain=Domain(
        domainType="PointSeries",
        axes={
            "x": {"dataType": "float", "values": [1.23]},
            "y": {"values": [4.56]},
            "t": {"dataType": "datetime", "values": [datetime.datetime.now()]},
        },
    ),
    ranges={"temperature": NdArray(axisNames=["x", "y", "t"], shape=[1, 1, 1], values=[42.0])},
)

pretty_print_json(c.json(exclude_none=True))
