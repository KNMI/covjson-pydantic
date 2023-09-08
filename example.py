from datetime import datetime
from datetime import timezone

from covjson_pydantic.coverage import Coverage
from covjson_pydantic.domain import Domain
from covjson_pydantic.ndarray import NdArray

c = Coverage(
    domain=Domain(
        domainType="PointSeries",
        axes={
            "x": {"dataType": "float", "values": [1.23]},
            "y": {"values": [4.56]},
            "t": {"dataType": "datetime", "values": [datetime.now(tz=timezone.utc)]},
        },
    ),
    ranges={"temperature": NdArray(axisNames=["x", "y", "t"], shape=[1, 1, 1], values=[42.0])},
)

print(c.model_dump_json(exclude_none=True, indent=4))
