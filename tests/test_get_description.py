import json

from src.mapunfold import get_description
import pytest

with open('tests/bps_names.json', 'r') as file:
    bps_names = json.load(file)


@pytest.mark.skip(reason="takes > 30 secs")
@pytest.mark.asyncio
async def test_get_description_runs():

    bps_name = bps_names[2]['bps_name']

    [prompt, description ] = await get_description(bps_name)

    print("prompt: ", prompt)
    print("description: ", description)

    assert description is not None