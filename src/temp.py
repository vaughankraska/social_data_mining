import pandas as pd
from sqlite3 import Connection
from src.config import get_db_connection
from src.crud import get_author_to_author


def get(db: Connection):
    authors = get_author_to_author(db, "retweeted")
    df = pd.DataFrame(authors)
    print(df.info())
    print(df.head())


def ingest_accounts(db: Connection, data_path: str = "data/accounts.tsv"):
    raise NotImplementedError


if __name__ == "__main__":
    db_connection = get_db_connection(use_dict_reponses=False)
    # ingest_tweets(db_connection, data_path="data/tweets.dat")
    get(db_connection)
    print("Done!!!")
    db_connection.close()
