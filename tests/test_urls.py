import json

import aiohttp
import pytest

from src.mapunfold import get_rampe_treppe_url


@pytest.mark.asyncio
async def test_async_call():
    with open('tests/bps_names.json', 'r') as file:
        bps_names = json.load(file)

    name = bps_names[6]["bps_name"]
    url = get_rampe_treppe_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.json()
            results = data["results"]
            assert len(results) > 0