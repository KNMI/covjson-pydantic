from typing import Annotated
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from covjson_pydantic.domain import Domain
from covjson_pydantic.ndarray import NdArray
from covjson_pydantic.ndarray import TiledNdArray
from pydantic import AnyUrl
from pydantic import Field
from pydantic import TypeAdapter

from .base_models import CovJsonBaseModel
from .domain import DomainType
from .parameter import Parameter
from .parameter import ParameterGroup
from .reference_system import ReferenceSystemConnectionObject


class Coverage(CovJsonBaseModel, extra="allow"):
    id: Optional[str] = None
    type: Literal["Coverage"] = "Coverage"
    domain: Domain
    parameters: Optional[Dict[str, Parameter]] = None
    parameterGroups: Optional[List[ParameterGroup]] = None  # noqa: N815
    ranges: Dict[str, Union[NdArray, TiledNdArray, AnyUrl]]


class CoverageCollection(CovJsonBaseModel, extra="allow"):
    type: Literal["CoverageCollection"] = "CoverageCollection"
    domainType: Optional[DomainType] = None  # noqa: N815
    coverages: List[Coverage]
    parameters: Optional[Dict[str, Parameter]] = None
    parameterGroups: Optional[List[ParameterGroup]] = None  # noqa: N815
    referencing: Optional[List[ReferenceSystemConnectionObject]] = None


CoverageJSON = TypeAdapter(
    Annotated[
        Union[CoverageCollection, Coverage, Domain, TiledNdArray, NdArray],
        Field(discriminator="type"),
    ]
)
