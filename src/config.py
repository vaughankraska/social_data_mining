import sqlite3
from sqlite3 import Connection

DB_NAME = "sdm.db"
db_connection: Connection = sqlite3.connect(DB_NAME)
