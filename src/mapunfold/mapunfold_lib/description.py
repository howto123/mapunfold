
from dataclasses import dataclass


@dataclass(frozen=True)
class Description:
    id: str
    en: str
    de: str
    fr: str
    it: str