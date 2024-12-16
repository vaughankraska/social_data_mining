from sdm.config import get_db_connection
from sdm.crud import ingest_accounts


def insert_accounts() -> None:
    print("Ingesting accounts")
    with get_db_connection(db_type="sqlite") as db:
        ingest_accounts(db)
        res = db.cursor().execute("SELECT COUNT(*) from accounts").fetchall()
        print(f"Accounts count: {res}")


def test() -> None:
    with get_db_connection(db_type="postgres") as db:
        with db.cursor() as cur:
            cur.execute("SELECT version()")
            print(cur.fetchone())


def main() -> None:
    print("Hello from sdm!")
