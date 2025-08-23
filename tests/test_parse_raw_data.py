from mapunfold import parse_raw_data


def test_parse_correct():

    # an example fitting the schema
    json_string = """
    {
        "Description": {
            "bps_name": "Berlin Hauptbahnhof",
            "en": "The Berlin Hauptbahnhof is a major railway station located in the heart of Berlin, Germany. It is situated on the north bank of the River Spree and serves as a hub for both national and international rail traffic. The station features several platforms, a large waiting area, and a variety of shops and restaurants. The geolocation of the station is { 'lon': 7.559610853184013, 'lat': 47.09541745748749 }.",
            "de": "Der Berlin Hauptbahnhof ist ein wichtiger Bahnhof in Berlin, Deutschland. Er liegt am Nordufer der Spree und dient als Knotenpunkt für nationale und internationale Eisenbahnverbindungen. Das Bahnhofsgebäude beherbergt mehrere Gleise, eine große Wartehalle und eine Vielzahl von Ladengeschäften und Restaurants. Die geografische Position des Bahnhofs ist { 'lon': 7.559610853184013, 'lat': 47.09541745748749 }.",
            "fr": "Le Berlin Hauptbahnhof est une gare importante situé dans le centre-ville de Berlin, en Allemagne. Elle se trouve sur la rive nord de l' River Spree et sert de nœud pour les trajets nationaux et internationaux. Le bâtiment de la gare abrite plusieurs plateformes, un grand espace d'attente et une variété de magasins et de restaurants. La position géographique de la gare est { 'lon': 7.559610853184013, 'lat': 47.09541745748749 }.",
            "it": "Il Berlin Hauptbahnhof è una stazione ferroviaria importante situata al centro della città di Berlino, in Germania. Si trova a nord del fiume Spree e funge da nodo per i collegamenti nazionali e internazionali. La stazione cuenta con diverse piattaforme, un'ampia area di attesa e una serie di negozi e ristoranti. La posizione geografica della stazione è { 'lon': 7.559610853184013, 'lat': 47.09541745748749 }."
        }
    }
    """
    description = parse_raw_data(json_string)
    pass
