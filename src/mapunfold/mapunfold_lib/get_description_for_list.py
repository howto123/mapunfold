from typing import List

from .get_description import get_description
from .description import Description


async def get_description_for_list(station_id_list: List[str]) -> List[Description]:
    result = []

    # we do the work for each station given
    for i in station_id_list:
        t = await get_description(i)
        result.append(t)

    return result