from typing import Union, Literal
import sqlite3
from sqlite3 import Connection as LiteConnection, Cursor
import psycopg
from psycopg import Connection as PostGresConnection

Connection = Union[LiteConnection, PostGresConnection]

DB_NAME = "data/twitter.db"
PG_NAME = "sdm"
PG_PASSWORD = "postgres"
PG_USER = "postgres"
PG_HOST = "localhost"
PG_PORT = 5432


def dict_factory(cursor: Cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db_connection(db_type: Literal["sqlite", "postgres"], **kwargs) -> Connection:
    """
    Get db connection to either 'slqite' or 'postgres'. Both use the DB-API
    protocol so it should work across the same queries (fingers crossed)
    Args:
        db_type (str): Type of database ('sqlite' or 'postgres').
        **kwargs: Database-specific connection parameters eg
        'db_path' and 'use_dict_responses' for sqlite.
    """

    if db_type == "sqlite":
        return get_lite_connection(
                db_path=kwargs.get("db_path", DB_NAME),
                use_dict_responses=kwargs.get("use_dict_responses", True)
                )
    elif db_type == "postgres":
        return get_pg_connection()
    else:
        raise ValueError(f"Unknown db_type '{db_type}'.")


def get_lite_connection(db_path: str, use_dict_responses: bool) -> LiteConnection:
    db_connection: Connection = sqlite3.connect(db_path)
    if use_dict_responses:
        db_connection.row_factory = dict_factory

    return db_connection


def get_pg_connection() -> PostGresConnection:
    """
    Returns a PostgreSQL connection using **psycopg3**.

    Usage:
        with get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone())
    """
    return psycopg.connect(
        dbname=PG_NAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
