import json

import aiohttp
import pytest

from src.mapunfold import *

with open('tests/bps_names.json', 'r') as file:
    bps_names = json.load(file)


@pytest.mark.asyncio
async def test_rampe_treppe_url():
    name = bps_names[6]["bps_name"]
    url = get_rampe_treppe_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.json()
            results = data["results"]
            assert len(results) > 0

@pytest.mark.asyncio
async def test_billetautomat_url():
    name = bps_names[5]["bps_name"]
    url = get_billetautomat_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.json()
            results = data["results"]
            assert len(results) > 0

@pytest.mark.asyncio
async def test_billetautomat_url():
    name = bps_names[3]["bps_name"]
    url = get_billetentwerter_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.json()
            results = data["results"]
            assert len(results) > 0