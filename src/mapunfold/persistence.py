import os

from src.mapunfold.mapunfold_lib import Description

import sqlite3

DEFAULT_DB_NAME = "mapunfold.db"


def store_to_db(descriptions: list[Description], sqlite_db_name: str = DEFAULT_DB_NAME):
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS descriptions (
            id TEXT PRIMARY KEY,
            en TEXT,
            de TEXT,
            fr TEXT,
            it TEXT
        )
    """)

    for desc in descriptions:
        cur.execute("""
                INSERT INTO descriptions (id, en, de, fr, it)
                VALUES (?, ?, ?, ?, ?)
            """, (desc.id, desc.en, desc.de, desc.fr, desc.it))

    con.commit()
    con.close()


def get_from_db(db_name: str = DEFAULT_DB_NAME) -> list[Description]:

    # it's the responsibility of the consumer to check arguments or handle this exception
    if not os.path.isfile(db_name):
        raise FileNotFoundError(db_name)

    con = sqlite3.connect(db_name)

    cur = con.cursor()

    # Fetch all rows from the descriptions table
    cur.execute("SELECT id, en, de, fr, it FROM descriptions")
    rows = cur.fetchall()

    # Close the connection
    con.close()

    # Convert each row into a Description object
    return [Description(*row) for row in rows]