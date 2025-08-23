
from dataclasses import dataclass


@dataclass(frozen=True)
class Description:
    bps_name: str
    en: str
    de: str
    fr: str
    it: str