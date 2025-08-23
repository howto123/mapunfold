


def get_rampe_treppe_url(bps_name: str) -> str:
    return f"https://data.sbb.ch/api/explore/v2.1/catalog/datasets/rampe-treppe/records?select=typ%2Cnutzung%2Chandlauf%2Cgeopos&where=bps_name%3D%22{bps_name}%22"


def get_billetautomat_url(bps_name: str) -> str:
    return f"https://data.sbb.ch/api/explore/v2.1/catalog/datasets/billetautomat/records?select=geopos&where=bps_name%3D%22{bps_name}%22&limit=20"