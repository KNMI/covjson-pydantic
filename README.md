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

Or install from source:

```shell
pip install git+https://github.com/KNMI/covjson-pydantic.git
```

## Usage

```python
from datetime import datetime, timezone
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
                "dataType": "float",
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
                "dataType": "datetime",
                "values": [
                    "2023-09-08T14:31:41.311717Z"
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

## Contributing

Make an editable install from within the repository root

```shell
pip install -e '.[test]'
```

### Running tests

```shell
pytest tests/
```

## Real world usage

This library is used to build an Environmental Data Retrieval (EDR) API, serving automatic weather data station data from the KNMI. See the [KNMI Data Platform](https://developer.dataplatform.knmi.nl/edr-api).

## TODOs
Help is wanted in the following areas to fully implement the CovJSON spec:
* The polygon based domain types are not supported.
* The `Trajectory` and `Section` domain type are not supported.
* The `NdArray` only supports `float` data.
* Not all requirements in the spec relating different fields are implemented.

## License

Apache License, Version 2.0

## Authors

Members of the KNMI Data Platform team. Reachable at opendata@knmi.nl.

## Copyright

Koninklijk Nederlands Meteorologisch Instituut (KNMI)
