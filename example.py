from datetime import datetime
from datetime import timezone

from covjson_pydantic.coverage import Coverage
from covjson_pydantic.domain import Axes
from covjson_pydantic.domain import Domain
from covjson_pydantic.domain import DomainType
from covjson_pydantic.domain import ValuesAxis
from covjson_pydantic.ndarray import NdArrayFloat
from pydantic import AwareDatetime

c = Coverage(
    domain=Domain(
        domainType=DomainType.point_series,
        axes=Axes(
            x=ValuesAxis[float](values=[1.23]),
            y=ValuesAxis[float](values=[4.56]),
            t=ValuesAxis[AwareDatetime](values=[datetime.now(tz=timezone.utc)]),
        ),
    ),
    ranges={"temperature": NdArrayFloat(axisNames=["x", "y", "t"], shape=[1, 1, 1], values=["42.0"])},
)

print(c.model_dump_json(exclude_none=True, indent=4))
