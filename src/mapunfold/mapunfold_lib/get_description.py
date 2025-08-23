import json

import aiohttp

from .description import Description
from .urls import *


# no property bps or bpsname -> ignored
# def get_dienststellen():
#     pass

async def get_treppen_and_ramps(bps_name: str):

    url = get_rampe_treppe_url(bps_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            results = data["results"]
            return results

# no bps or bps_name -> ignored
# def get_wartehallen():
#     pass

# sektortafel -> according to discord, this is not relevant, ignored

async def get_billetautomat(bps_name: str):

    url = get_billetautomat_url(bps_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            results = data["results"]
            return results

async def get_billetentwerter(bps_name: str):

    url = get_billetentwerter_url(bps_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            results = data["results"]
            return results

async def get_sid(bps_name: str):

    url = get_sid_url(bps_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            results = data["results"]
            return results



def pull_info_together(treppen_and_rampen, billetautomats, billetentwerters, sids):

    obj = {}

    obj["treppen_and_rampen"] = treppen_and_rampen
    obj["billetautomats"] = billetautomats
    obj["billetentwerters"] = billetentwerters
    obj["sids"] = sids

    return obj


async def gather_info(bps_name):

    treppen_and_rampen = await get_treppen_and_ramps(bps_name)
    billetautomats = await get_billetautomat(bps_name)
    billetentwerters = await get_billetentwerter(bps_name)
    sids = await get_sid(bps_name)

    info = pull_info_together(treppen_and_rampen, billetautomats, billetentwerters, sids)

    return info





    # info = pull_info_together(info_open_transport_data, info_open_street_map, info_insa_export_api)
    # return info


async def create_texts(info):
    raise NotImplementedError()


async def get_description(bps_name: str) -> Description:

    info = await gather_info(bps_name)
    result = await create_texts(info)
    return result