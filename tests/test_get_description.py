import json

from src import mapunfold
import pytest

with open('tests/bps_names.json', 'r') as file:
    bps_names = json.load(file)

@pytest.mark.asyncio
async def test_get_description_runs():

    bps_name = bps_names[2]['bps_name']

    description = await mapunfold.get_description(bps_name)

    assert description is not None