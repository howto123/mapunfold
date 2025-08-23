from .description import Description


def get_open_transport_info():
    pass


def get_osm_info():
    pass


def get_insa_export_info():
    pass


def pull_info_together(info_open_transport_data, info_open_street_map, info_insa_export_api):
    pass


async def gather_info(id):


    info_open_transport_data = get_open_transport_info()

    info_open_street_map = get_osm_info()

    info_insa_export_api = get_insa_export_info()





    info = pull_info_together(info_open_transport_data, info_open_street_map, info_insa_export_api)
    return info


async def create_texts(info):
    pass


async def get_description(station_id: str) -> Description:

    info = await gather_info(station_id)
    result = await create_texts(info)
    return result