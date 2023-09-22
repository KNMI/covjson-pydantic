from enum import Enum
from typing import Dict


class LanguageTag(str, Enum):
    dutch = "nl"
    english = "en"
    german = "de"
    undefined = "und"


# TODO: This was throwing warning:
#   Expected `definition-ref` but got `LanguageTag` - serialized value may not be as expected
# This may be a bug in Pydantic: https://github.com/pydantic/pydantic/issues/6467
# or: https://github.com/pydantic/pydantic/issues/6422
# So, for now, reverted to a less strict type
# See issue: https://github.com/KNMI/covjson-pydantic/issues/3
# i18n = Dict[LanguageTag, str]
i18n = Dict[str, str]
