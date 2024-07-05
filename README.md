# CoverageJSON Pydantic

<p>
  <a href="https://github.com/knmi/covjson-pydantic/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/knmi/covjson-pydantic/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/knmi/covjson-pydantic" target="_blank">
      <img src="https://codecov.io/gh/knmi/covjson-pydantic/branch/master/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/covjson-pydantic" target="_blank">
      <img src="https://img.shields.io/pypi/v/covjson-pydantic?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypistats.org/packages/covjson-pydantic" target="_blank">
      <img src="https://img.shields.io/pypi/dm/covjson-pydantic.svg" alt="Downloads">
  </a>
  <a href="https://github.com/knmi/covjson-pydantic/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/knmi/covjson-pydantic.svg" alt="License">
  </a>
</p>


This repository contains the coveragejson-pydantic Python package. It provides [Pydantic](https://pydantic-docs.helpmanual.io/) models for [CoverageJSON](https://covjson.org/). This can, for example, be used to develop an API using FastAPI serving or receiving CoverageJSON.

## Install
```shell
pip install covjson-pydantic
```

Or you can install directly from source:

```shell
pip install git+https://github.com/KNMI/covjson-pydantic.git
```

## Usage

### Generating CovJSON

```python
from datetime import datetime, timezone
from pydantic import AwareDatetime
from covjson_pydantic.coverage import Coverage
from covjson_pydantic.domain import Domain, Axes, ValuesAxis, DomainType
from covjson_pydantic.ndarray import NdArray

c = Coverage(
    domain=Domain(
        domainType=DomainType.point_series,
        axes=Axes(
            x=ValuesAxis[float](values=[1.23]),
            y=ValuesAxis[float](values=[4.56]),
            t=ValuesAxis[AwareDatetime](values=[datetime.now(tz=timezone.utc)])
        )
    ),
    ranges={
        "temperature": NdArray(axisNames=["x", "y", "t"], shape=[1, 1, 1], values=[42.0])
    }
)

print(c.model_dump_json(exclude_none=True, indent=4))
```
Will print
```json
{
    "type": "Coverage",
    "domain": {
        "type": "Domain",
        "domainType": "PointSeries",
        "axes": {
            "x": {
                "values": [
                    1.23
                ]
            },
            "y": {
                "values": [
                    4.56
                ]
            },
            "t": {
                "values": [
                    "2023-09-14T11:54:02.151493Z"
                ]
            }
        }
    },
    "ranges": {
        "temperature": {
            "type": "NdArray",
            "dataType": "float",
            "axisNames": [
                "x",
                "y",
                "t"
            ],
            "shape": [
                1,
                1,
                1
            ],
            "values": [
                42.0
            ]
        }
    }
}
```

### Validating CovJSON

There is a helper `TypeAdapter` called `CoverageJSON` that will validate any (supported) CoverageJSON input, and
return the corresponding model. These can be of the type `CoverageCollection`, `Coverage`, `Domain`, `TiledNdArray`
or `NdArray`.

```python
from covjson_pydantic.coverage import CoverageJSON
covjson = CoverageJSON.validate_json("""
{
    "type": "NdArray",
    "dataType": "float",
    "axisNames": [
        "t",
        "y",
        "x"
    ],
    "shape": [
        1,
        1,
        1
    ],
    "values": [
        27.1
    ]
}
""")
print(type(covjson))
```

## Contributing

Make an editable installation from within the repository root

```shell
pip install -e '.[test]'
```

### Running tests

```shell
pytest tests/
```

### Linting and typing

Linting and typing (mypy) is done using [pre-commit](https://pre-commit.com) hooks.

```shell
pip install pre-commit
pre-commit install
pre-commit run
```

## Related packages

* [edr-pydantic](https://github.com/KNMI/edr-pydantic) - Pydantic data models for the Environmental Data Retrieval (EDR) API
* [geojson-pydantic](https://github.com/developmentseed/geojson-pydantic) - Pydantic data models for the GeoJSON spec

## Real world usage

This library is used to build an OGC Environmental Data Retrieval (EDR) API, serving automatic weather data station data from The Royal Netherlands Meteorological Institute (KNMI). See the [KNMI Data Platform EDR API](https://developer.dataplatform.knmi.nl/edr-api).

## TODOs
Help is wanted in the following areas to fully implement the CovJSON spec:
* The polygon based domain types are not supported.
* The `Trajectory` and `Section` domain type are not supported.
* The `NdArray` only supports `float` data.
* Not all requirements in the spec relating different fields are implemented.

## License

Apache License, Version 2.0
