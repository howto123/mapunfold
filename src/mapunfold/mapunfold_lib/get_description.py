from .description import Description


async def gather_info(id):
    pass


async def create_texts(info):
    pass


async def get_description(station_id: str) -> Description:

    info = await gather_info(station_id)
    result = await create_texts(info)
    return result