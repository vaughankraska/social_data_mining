from sdm.config import get_db_connection
from sdm.crud import ingest_accounts
from sdm.crud import ingest_tweets, ingest_reddit


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
        with db.cursor() as cur:
            res = cur.execute("""
            SELECT text AS length
            FROM submissions
            ORDER BY LENGTH(text) DESC
            LIMIT 1;
            """)
            print(res.fetchone())


def main() -> None:
    print("Hello from sdm!")
