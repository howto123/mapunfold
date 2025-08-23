from src import mapunfold
import pytest

@pytest.mark.asyncio
async def test_get_description_runs():

    id = "invented"

    await mapunfold.get_description(id)