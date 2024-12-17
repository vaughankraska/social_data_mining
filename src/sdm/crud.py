import pandas as pd
import sqlite3
from sdm.utils import tweets_as_dataframe
from sdm.config import Connection
from typing import List, Dict, Any


def get_all_tweets(db: Connection) -> List[Dict[str, Any]]:
    cur = db.cursor()
    res = cur.execute("SELECT * FROM tweets")
    return res.fetchall()


def get_all_reference_tweets(db: Connection) -> List[Dict[str, Any]]:
    cur = db.cursor()
    res = cur.execute("SELECT * FROM referenced_tweets")
    return res.fetchall()


def get_distinct_authors(db: Connection) -> List[str]:
    cur = db.cursor()
    res = cur.execute("SELECT DISTINCT author_id FROM tweets")
    return [value["author_id"] for value in res.fetchall()]


def get_author_to_author(db: Connection, response_type: str = "retweeted"):
    """Possible response types are: 'retweeted' | 'replied_to' | 'quoted'"""
    cur = db.cursor()
    query = """
    SELECT
        t1.author_id as from_author,
        t2.author_id as to_author
    FROM tweets t1
    JOIN referenced_tweets rt ON t1.id = rt.tweet_id
    JOIN tweets t2 ON rt.referenced_tweet_id = t2.id
    WHERE
        rt.referenced_tweet_type = ?
        AND t1.author_id != t2.author_id
    """
    res = cur.execute(query, [response_type])

    return res.fetchall()


def create_tweets_table(db: Connection):
    cur = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            text TEXT,
            author_id TEXT,
            created_at TEXT,
            possibly_sensitive BOOLEAN,
            lang TEXT,
            conversation_id TEXT,
            public_metrics TEXT,
            attachments TEXT,
            in_reply_to_user_id TEXT,
            geo TEXT,
            withheld TEXT,
            entities TEXT,
            context_annotations TEXT
            )
    """
    cur.execute(query)


def create_ref_tweets_table(db: Connection):
    cur = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS referenced_tweets (
            tweet_id TEXT,
            referenced_tweet_id TEXT,
            referenced_tweet_type TEXT,
            FOREIGN KEY (tweet_id) REFERENCES tweets(id)
            )
    """
    cur.execute(query)


def create_accounts_table(db: Connection):
    cur = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS accounts (
            author_id TEXT PRIMARY KEY,
            account_type TEXT,
            lang TEXT,
            stance TEXT --, FOREIGN KEY (author_id) REFERENCES tweets(author_id)
            )
    """
    cur.execute(query)


def create_submissions_table(db: Connection):
    if isinstance(db, sqlite3.Connection):
        raise ValueError("Sqlite Connection not allowed.")
    with db.cursor() as cur:
        query = """
        CREATE TABLE IF NOT EXISTS submissions (
            submission_id VARCHAR PRIMARY KEY,
            redditor_id VARCHAR,
            created_at TIMESTAMPTZ,
            title VARCHAR,
            text TEXT,
            subreddit VARCHAR,
            permalink VARCHAR,
            attachment JSONB,
            flair JSONB,
            awards JSONB,
            score JSONB,
            upvote_ratio JSONB,
            num_comments JSONB,
            edited BOOLEAN,
            archived BOOLEAN,
            removed BOOLEAN,
            poll JSONB
        )
        """
        cur.execute(query)


def create_comments_table(db: Connection):
    if isinstance(db, sqlite3.Connection):
        raise ValueError("Sqlite Connection not allowed.")
    with db.cursor() as cur:
        query = """
        CREATE TABLE IF NOT EXISTS comments (
            comment_id VARCHAR PRIMARY KEY,
            link_id VARCHAR,
            subreddit VARCHAR,
            parent_id VARCHAR,
            redditor_id VARCHAR,
            created_at TIMESTAMPTZ,
            body TEXT,
            score JSONB,
            edited BOOLEAN,
            removed VARCHAR
        );
        """
        cur.execute(query)


def ingest_comments(
        db: Connection,
        data_path: str = "data/commments.csv",
        chunk_size: int = 10_000
        ):
    df = pd.read_csv(data_path)
    print("[*] Ingesting comments from")
    print(df.info())
    with db.cursor() as cur:
        query = """
        INSERT INTO comments (
            comment_id,
            link_id,
            subreddit,
            parent_id,
            redditor_id,
            created_at,
            body,
            score,
            edited,
            removed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i : i + chunk_size].values.tolist()
            cur.executemany(query, chunk)
            db.commit()
    print("[*] Inserted comments")


def ingest_submissions(
        db: Connection,
        data_path: str = "data/submission.csv",
        chunk_size: int = 10_000
        ):

    df = pd.read_csv(data_path)
    df['poll'] = df['poll'].where(pd.notna(df['poll']), "{}")
    df['attachment'] = df['attachment'].where(pd.notna(df['attachment']), "{}")

    print("[*] Ingesting submissions from")
    print(df.info())
    with db.cursor() as cur:
        query = """
        INSERT INTO submissions (
            submission_id,
            redditor_id,
            created_at,
            title,
            text,
            subreddit,
            permalink,
            attachment,
            flair,
            awards,
            score,
            upvote_ratio,
            num_comments,
            edited,
            archived,
            removed,
            poll
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i : i + chunk_size].values.tolist()
            cur.executemany(query, chunk)
            db.commit()
    print("[*] Inserted submissions")


def ingest_reddit(
        db: Connection,
        comments_path: str = "data/commments.csv",
        submissions_path: str = "data/submission.csv",
        chunk_size: int = 10_000
        ):
    create_submissions_table(db)
    create_comments_table(db)
    ingest_submissions(db, data_path=submissions_path)
    ingest_comments(db, data_path=comments_path)
    print("[*] REddiT INGesT ComplEtE!")


def ingest_accounts(
    db: Connection, data_path: str = "data/accounts.tsv", chunk_size: int = 10_000
):
    df = pd.read_csv(data_path, delimiter="\t", dtype={"author_id": str})
    df["author_id"] = df["author_id"].astype(str)
    print(df.info())
    create_accounts_table(db)

    query = """
    INSERT INTO accounts (
            author_id,
            account_type,
            lang,
            stance
            )
    VALUES (?, ?, ?, ?)
    """
    cur = db.cursor()
    for i in range(0, len(df), chunk_size):
        chunk_values = df.iloc[i : i + chunk_size].values.tolist()
        cur.executemany(query, chunk_values)
        db.commit()
    print("[*] Inserted accounts")


def ingest_tweets(
    db: Connection, data_path: str = "data/tweets.dat", chunk_size=100_000
):
    print()
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
    df = df.join(
        pd.DataFrame(df["referenced_tweets"].dropna().explode().tolist()).add_prefix(
            "rt_"
        ),
    )

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i : i + chunk_size]
        tweets_chunk = chunk[tweets_columns].values.tolist()
        rt_chunk = chunk[["id", "rt_id", "rt_type"]].dropna().values.tolist()
        cur.executemany(tweet_query, tweets_chunk)
        cur.executemany(rt_query, rt_chunk)
        db.commit()

    res = cur.execute("SELECT COUNT(*) as n from tweets")
    print(f"Tweets rows = {res.fetchone()}")
    res = cur.execute("SELECT COUNT(*) as n from referenced_tweets")
    print(f"Ref Tweets rows = {res.fetchone()}")
