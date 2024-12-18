import json
import requests
import pandas as pd
from typing import Literal
from sdm.config import Connection


def get_all_embeddings(db: Connection) -> pd.DataFrame:
    """Get embeddings and the original text."""
    tebs = get_tweet_embeddings(db)
    cebs = get_comment_embeddings(db)
    sebs = get_submission_embeddings(db)

    df_all = pd.concat([tebs, cebs, sebs], axis=0, ignore_index=True)

    return df_all


def get_tweet_embeddings(db: Connection) -> pd.DataFrame:
    with db.cursor() as cur:
        res = cur.execute("""
        SELECT
            e.id, t.text AS text, e.doc_type, e.doc_id, e.embedding
        FROM
            embeddings e
        JOIN
            tweets t
        ON
            e.doc_id = t.id
        WHERE
            doc_type = 'tweet'
        """).fetchall()
    df = pd.DataFrame(res)
    df["embedding"] = df["embedding"].apply(lambda t: json.loads(t))
    return df


def get_comment_embeddings(db: Connection) -> pd.DataFrame:
    with db.cursor() as cur:
        res = cur.execute("""
        SELECT
            e.id, c.body AS text, e.doc_type, e.doc_id, e.embedding
        FROM
            embeddings e
        JOIN
            comments c
        ON
            e.doc_id = c.comment_id
        WHERE
            doc_type = 'comment'
        """).fetchall()
    df = pd.DataFrame(res)
    df["embedding"] = df["embedding"].apply(lambda t: json.loads(t))
    return df


def get_submission_embeddings(db: Connection) -> pd.DataFrame:
    with db.cursor() as cur:
        res = cur.execute("""
        SELECT
            e.id, s.text AS text, e.doc_type, e.doc_id, e.embedding
        FROM
            embeddings e
        JOIN
            submissions s
        ON
            e.doc_id = s.submission_id
        WHERE
            doc_type = 'submission'
        """).fetchall()
    df = pd.DataFrame(res)
    df["embedding"] = df["embedding"].apply(lambda t: json.loads(t))
    return df


def create_embeddings_table(db: Connection):
    with db.cursor() as cur:
        cur.execute("""
        CREATE EXTENSION IF NOT EXISTS vector
        """)

        cur.execute("""
        DROP TYPE IF EXISTS DOC_TYPE;
        CREATE TYPE DOC_TYPE AS ENUM ('tweet', 'submission', 'comment');
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id bigserial PRIMARY KEY,
            doc_type DOC_TYPE NOT NULL,
            doc_id TEXT NOT NULL UNIQUE,
            embedding vector(768)
            )
        """)


def embed_doc(
        db: Connection,
        text: str,
        doc_id: str,
        doc_type: Literal["tweet", "submission", "comment"]
        ):

    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "paraphrase-multilingual",
        "prompt": text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        embedding = response.json()["embedding"]
        query = """
        INSERT INTO embeddings (
                doc_type,
                doc_id,
                embedding
                )
        VALUES (?, ?, ?)
        """

        with db.cursor() as cur:
            cur.execute(query, [doc_type, doc_id, embedding])
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)


def embed_tweets(db: Connection):
    with db.cursor() as cur:
        tweets = cur.execute("""
           SELECT
               DISTINCT ON (t.text) a.author_id,
               t.id,
               t.text,
               a.author_id AS account_id,
               t.created_at,
               a.account_type,
               a.lang
           FROM
               accounts a
           JOIN
               tweets t
           ON
               a.author_id = t.author_id
           WHERE
               (a.lang = 'en' OR a.lang = 'fr')
               AND a.account_type IN ('Private individuals', 'Business actors')
        """).fetchall()
    inserted_count = 0
    total = len(tweets)
    for idx, tweet in enumerate(tweets):
        if idx % 99 == 0:
            print(f"[*] Tweet {idx}/{total}")
        try:
            embed_doc(db, text=tweet["text"], doc_id=tweet["id"], doc_type="tweet")
            inserted_count += 1
        except Exception as e:
            print("[!] Failed to insert tweet:", tweet)
            print("[!] Due to: ", e)


def embed_comments(db: Connection):
    with db.cursor() as cur:
        comments = cur.execute("""
           SELECT
               DISTINCT body AS text,
               comment_id as id
           FROM
               comments
        """).fetchall()
    inserted_count = 0
    total = len(comments)
    for idx, comm in enumerate(comments):
        if idx % 99 == 0:
            print(f"[*] Comment {idx}/{total}")
        try:
            embed_doc(db, text=comm["text"], doc_id=comm["id"], doc_type="comment")
            inserted_count += 1
        except Exception as e:
            print("[!] Failed to insert comment:", comm)
            print("[!] Due to: ", e)


def embed_submissions(db: Connection):
    with db.cursor() as cur:
        submissions = cur.execute("""
           SELECT
               DISTINCT text AS text,
               submission_id as id
           FROM
               submissions
        """).fetchall()
    inserted_count = 0
    total = len(submissions)
    for idx, sub in enumerate(submissions):
        if idx % 99 == 0:
            print(f"[*] Submission {idx}/{total}")
        try:
            embed_doc(db, text=sub["text"], doc_id=sub["id"], doc_type="submission")
            inserted_count += 1
        except Exception as e:
            print("[!] Failed to insert submission:", sub)
            print("[!] Due to: ", e)
