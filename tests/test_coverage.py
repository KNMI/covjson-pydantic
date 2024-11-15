import json
from pathlib import Path

import pytest
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.coverage import CoverageCollection
from covjson_pydantic.domain import Axes
from covjson_pydantic.domain import Domain
from covjson_pydantic.ndarray import NdArray
from covjson_pydantic.ndarray import NdArrayFloat
from covjson_pydantic.ndarray import NdArrayInt
from covjson_pydantic.ndarray import NdArrayStr
from covjson_pydantic.ndarray import TiledNdArray
from covjson_pydantic.parameter import Parameter
from covjson_pydantic.parameter import ParameterGroup
from covjson_pydantic.reference_system import ReferenceSystem
from pydantic import ValidationError


happy_cases = [
    ("spec-axes.json", Axes),
    ("str-axes.json", Axes),
    ("coverage-json.json", Coverage),
    ("coverage-mixed-type-ndarray.json", Coverage),
    ("doc-example-coverage.json", Coverage),
    ("spec-vertical-profile-coverage.json", Coverage),
    ("spec-trajectory-coverage.json", Coverage),
    ("doc-example-coverage-collection.json", CoverageCollection),
    ("grid-domain.json", Domain),
    ("point-series-domain-custom.json", Domain),
    ("spec-domain-grid.json", Domain),
    ("spec-domain-vertical-profile.json", Domain),
    ("spec-domain-point-series.json", Domain),
    ("spec-domain-point.json", Domain),
    ("spec-domain-point-compact.json", Domain),
    ("spec-domain-multipoint-series.json", Domain),
    ("spec-domain-multipoint.json", Domain),
    ("spec-domain-trajectory.json", Domain),
    ("ndarray-float.json", NdArrayFloat),
    ("ndarray-string.json", NdArrayStr),
    ("ndarray-integer.json", NdArrayInt),
    ("spec-ndarray.json", NdArrayFloat),
    ("spec-tiled-ndarray.json", TiledNdArray),
    ("continuous-data-parameter.json", Parameter),
    ("categorical-data-parameter.json", Parameter),
    ("spec-parametergroup.json", ParameterGroup),
    ("spec-reference-system-identifierrs.json", ReferenceSystem),
]


@pytest.mark.parametrize("file_name, object_type", happy_cases)
def test_happy_cases(file_name, object_type):
    file = Path(__file__).parent.resolve() / "test_data" / file_name
    # Put JSON in default unindented format
    with open(file, "r") as f:
        data = json.load(f)
    json_string = json.dumps(data, separators=(",", ":"))

    # Round-trip
    assert object_type.model_validate_json(json_string).model_dump_json(exclude_none=True) == json_string


error_cases = [
    ("grid-domain-no-y.json", Domain, r"A 'Grid' must have a 'y'-axis"),
    (
        "point-series-domain-more-z.json",
        Domain,
        r"If provided, the 'values' field of the ValuesAxis 'z'-axis of a 'PointSeries' "
        + "domain must contain a single value.",
    ),
    ("point-series-domain-no-t.json", Domain, r"A 'PointSeries' must have a 't'-axis."),
    ("mixed-type-axes.json", Axes, r"Input should be a valid number"),
    ("mixed-type-axes-2.json", Axes, r"Input should be a valid string"),
    ("mixed-type-ndarray-1.json", NdArrayFloat, r"Input should be a valid number"),
    ("mixed-type-ndarray-2.json", NdArrayStr, r"Input should be 'string'"),
    ("mixed-type-ndarray-3.json", NdArrayInt, r"Input should be a valid integer"),
    ("mixed-type-ndarray-3.json", NdArrayFloat, r"Input should be 'float'"),
]


@pytest.mark.parametrize("file_name, object_type, error_message", error_cases)
def test_error_cases(file_name, object_type, error_message):
    file = Path(__file__).parent.resolve() / "test_data" / file_name
    # Put JSON in default unindented format
    with open(file, "r") as f:
        data = json.load(f)
    json_string = json.dumps(data, separators=(",", ":"))

    with pytest.raises(ValidationError, match=error_message):
        object_type.model_validate_json(json_string)


def test_ndarray_directly():
    with pytest.raises(TypeError, match="NdArray cannot be instantiated directly"):
        NdArray(axisNames=["x", "y", "t"], shape=[1, 1, 1], values=[42.0])
