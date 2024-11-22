import timeit
from pathlib import Path

filename = Path(__file__).parent.resolve() / "tests" / "test_data" / "coverage-json.json"

setup = f"""
import json
from covjson_pydantic.coverage import Coverage

file = "{filename}"
# Put JSON in default unindented format
with open(file, "r") as f:
    data = json.load(f)
json_string = json.dumps(data, separators=(",", ":"))
cj = Coverage.model_validate_json(json_string)
"""

# This can be used to quickly check performance. The first call checks JSON to Python conversion
# The second call checks Python to JSON conversion
# Consider generating a larger CoverageJSON file
print(timeit.timeit("Coverage.model_validate_json(json_string)", setup, number=1000))
print(timeit.timeit("cj.model_dump_json(exclude_none=True)", setup, number=1000))
