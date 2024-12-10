from sdm.config import get_db_connection
from sdm.crud import ingest_accounts
from text_mining.data import get_tweet_corpora


def insert_accounts() -> None:
    print("Ingesting accounts")
    db = get_db_connection()
    ingest_accounts(db)
    res = db.cursor().execute("SELECT COUNT(*) from accounts").fetchall()
    print(f"Accounts count: {res}")


def test() -> None:
    db = get_db_connection()
    min_chars = 100
    df = get_tweet_corpora(db, min_chars=min_chars)
    print(df.info())
    print(df.head())


def main() -> None:
    print("Hello from sdm!")
