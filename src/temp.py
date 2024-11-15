import pandas as pd
from sqlite3 import Connection
from src.config import db_connection
from src.utils import tweets_as_dataframe
from src.crud import create_tweets_table, create_ref_tweets_table


def ingest_tweets(
    db: Connection, data_path: str = "data/tweets.dat", chunk_size=100_000
):
    create_tweets_table(db)
    create_ref_tweets_table(db)
    cur = db.cursor()
    tweets_columns = [
        "id",
        "text",
        "author_id",
        "created_at",
        "possibly_sensitive",
        "lang",
        "conversation_id",
        "public_metrics",
        "attachments",
        "in_reply_to_user_id",
        "geo",
        "withheld",
        "entities",
        "context_annotations",
    ]

    tweet_query = f"""
    INSERT INTO tweets ({', '.join(tweets_columns)})
    VALUES ({', '.join('?' for _ in tweets_columns)})
    """

    rt_query = """
    INSERT INTO referenced_tweets (
            tweet_id,
            referenced_tweet_id,
            referenced_tweet_type
            )
    VALUES (?, ?, ?)
    """
    print(f"query:\n'{tweet_query}'\n rt:\n{rt_query}")
    possibly_problematic = [
        "public_metrics",
        "attachments",
        "geo",
        "withheld",
        "entities",
        "context_annotations",
    ]

    df = tweets_as_dataframe(file_path=data_path)
    df[possibly_problematic] = df[possibly_problematic].astype(str)
    # df_rt = pd.DataFrame(df["referenced_tweets"].tolist(), index=df["id"])
    # print(df_rt.info())
    # print(df_rt.head())
    for i in range(0, len(df), chunk_size):
        tweets_chunk = df[tweets_columns].iloc[i:i + chunk_size].values.tolist()
        rt_chunk = df["referenced_tweets"].iloc[i:i + chunk_size].values.tolist()
        # rt_chunk is 20_000 arrays of lists of dicts
        cur.executemany(tweet_query, tweets_chunk)
        db.commit()

    res = cur.execute("SELECT COUNT(*) from tweets")
    print(f"Tweets rows = {res.fetchone()[0]}")
    res = cur.execute("SELECT COUNT(*) from referenced_tweets")
    print(f"Ref Tweets rows = {res.fetchone()[0]}")


def ingest_accounts(db: Connection, data_path: str = "data/accounts.tsv"):
    pass


if __name__ == "__main__":
    ingest_tweets(db_connection, data_path="data/tweets_small.dat")
    print("Done!!!")
