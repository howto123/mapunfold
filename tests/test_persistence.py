
import pytest
import os

from src.mapunfold import Description
from src.mapunfold.persistence import store_to_db, get_from_db

example_descriptions: list[Description] = [
    Description("1", "Apple", "Apfel", "Pomme", "Mela"),
    Description("2", "Car", "Auto", "Voiture", "Macchina"),
    Description("3", "House", "Haus", "Maison", "Casa"),
    Description("4", "Book", "Buch", "Livre", "Libro"),
    Description("5", "Dog", "Hund", "Chien", "Cane"),
    Description("6", "Cat", "Katze", "Chat", "Gatto"),
    Description("7", "Tree", "Baum", "Arbre", "Albero"),
    Description("8", "Water", "Wasser", "Eau", "Acqua"),
    Description("9", "Sun", "Sonne", "Soleil", "Sole"),
    Description("10", "Moon", "Mond", "Lune", "Luna"),
]

db_name = "test.db"

@pytest.fixture()
def setup():
    if os.path.isfile(db_name):
        os.remove(db_name)


def test_database_created(setup):
    store_to_db(example_descriptions, db_name)

    assert os.path.isfile(db_name)

def test_store_and_retreieve(setup):
    store_to_db(example_descriptions, db_name)
    items = get_from_db(db_name)

    assert len(items) == len(example_descriptions)
    assert set(items) == set(example_descriptions)