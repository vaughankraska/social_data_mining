from sdm.config import get_db_connection
from sdm.crud import ingest_accounts


def insert_accounts() -> None:
    print("Ingesting accounts")
    db = get_db_connection()
    ingest_accounts(db)
    res = db.cursor().execute("SELECT COUNT(*) from accounts").fetchall()
    print(f"Accounts count: {res}")


def main() -> None:
    print("Hello from sdm!")
