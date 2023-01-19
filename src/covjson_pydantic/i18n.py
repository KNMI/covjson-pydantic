from enum import Enum
from typing import Dict


class LanguageTag(str, Enum):
    dutch = "nl"
    english = "en"
    german = "de"
    undefined = "und"


i18n = Dict[LanguageTag, str]
