from src.mapunfold.persistence import store_to_db

example_descriptions = []

def test_database_created():
    store_to_db(example_descriptions)