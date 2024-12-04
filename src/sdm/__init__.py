import pandas as pd
from sdm.config import get_db_connection
from sdm.crud import ingest_accounts


def insert_accounts() -> None:
    print("Ingesting accounts")
    db = get_db_connection()
    ingest_accounts(db)
    res = db.cursor().execute("SELECT COUNT(*) from accounts").fetchall()
    print(f"Accounts count: {res}")


def test() -> None:
    db = get_db_connection()
    res = db.execute("""
               SELECT
                   a.author_id AS account_id,
                   t.text AS tweet_text,
                   a.account_type,
                   a.lang,
                   a.stance
               FROM
                   accounts a
               JOIN
                   tweets t
               ON
                   a.author_id = t.author_id
               WHERE
                   a.lang = 'en'
                   AND a.account_type IN ('Private individuals', 'Business actors')
               """).fetchall()
    df = pd.DataFrame(res)
    print(df.info())
    print(df.head())

def main() -> None:
    print("Hello from sdm!")
