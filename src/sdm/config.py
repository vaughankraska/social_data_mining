import sqlite3
from sqlite3 import Connection, Cursor

DB_NAME = "data/twitter.db"


def dict_factory(cursor: Cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db_connection(db_path: str = DB_NAME, use_dict_reponses=True):
    db_connection: Connection = sqlite3.connect(db_path)
    if use_dict_reponses:
        db_connection.row_factory = dict_factory

    return db_connection
