import aiohttp
import pytest

from src import mapunfold


# fixtures;
# @pytest.fixture
# @pytest_asyncio.fixture


@pytest.mark.asyncio
async def test_mapunfold_runs():

    await mapunfold.main()


@pytest.mark.asyncio
async def test_async_call():
    target = "https://api.insa.geops.ch/export/geo/stations/8507000/services"
    async with aiohttp.ClientSession() as session:
        async with session.get(target) as response:
            text = await response.text()
            assert response.status == 200
            print(text)
