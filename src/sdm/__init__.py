from sdm.config import get_db_connection
from sdm.crud import ingest_reddit, ingest_tweets, ingest_accounts
from sdm.crud_embeddings import (
        create_embeddings_table,
        embed_tweets,
        embed_comments,
        embed_submissions,
        embed_clean_tweets,
        embed_clean_comments,
        embed_clean_submissions
        )


def insert_accounts() -> None:
    print("Ingesting accounts")
    with get_db_connection(db_type="sqlite") as db:
        ingest_accounts(db)
        res = db.cursor().execute("SELECT COUNT(*) from accounts").fetchall()
        print(f"Accounts count: {res}")


def ingest_pg() -> None:
    # ingres tweets
    with get_db_connection(db_type="postgres") as db:
        ingest_tweets(db)
    # ingres accounts
    with get_db_connection(db_type="postgres") as db:
        ingest_accounts(db)
    # ingres reddit
    with get_db_connection(db_type="postgres") as db:
        ingest_reddit(db)


def test() -> None:
    # embeddings
    with get_db_connection(db_type="postgres") as db:
        # create_embeddings_table(db)
        # embed_comments(db)
        # embed_submissions(db)
        # embed_tweets(db)
        # embed_clean_tweets(db)
        # embed_clean_comments(db)
        embed_clean_submissions(db)

        print("Embedded tweeets!!!")


def main() -> None:
    print("Hello from sdm!")
