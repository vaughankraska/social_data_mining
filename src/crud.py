from sqlite3 import Connection
from typing import Dict, Any


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
