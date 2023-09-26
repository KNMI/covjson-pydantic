from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import AnyUrl

from .base_models import CovJsonBaseModel
from .domain import Domain
from .domain import DomainType
from .ndarray import NdArray
from .ndarray import TiledNdArray
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
