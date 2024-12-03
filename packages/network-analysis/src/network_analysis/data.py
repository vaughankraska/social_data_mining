import pandas as pd
from sqlite3 import Connection


def common_ideology(db: Connection, seconds_between: int, save_csv: bool = False):
    cur = db.cursor()

    cur.execute("""
        CREATE TEMP TABLE tweet_urls AS
        SELECT
            tweets.id,
            tweets.text,
            tweets.author_id,
            json_extract(value, '$.expanded_url') AS url,
            tweets.lang,
            tweets.possibly_sensitive,
            datetime(created_at) AS created_at
        FROM tweets,
            json_each(json_extract(entities, '$.urls'))
        WHERE
            json_extract(entities, '$.urls') IS NOT NULL
        AND text NOT LIKE 'RT @%'
    """)

    # Create indexes for speed
    cur.execute("CREATE INDEX temp.idx_tweet_urls_url ON tweet_urls(url)")
    cur.execute("CREATE INDEX temp.idx_tweet_langs ON tweet_urls(lang)")
    cur.execute("CREATE INDEX temp.idx_tweet_urls_id ON tweet_urls(id)")
    cur.execute("CREATE INDEX temp.idx_tweet_urls_author ON tweet_urls(author_id)")
    cur.execute(
        "CREATE INDEX temp.idx_tweet_urls_combined ON tweet_urls(url, id, author_id)"
    )

    res = cur.execute(
        """
        SELECT
            t1.id AS id1,
            t2.id AS id2,
            t1.url,
            t1.text AS text1,
            t2.text AS text2,
            t1.lang as lang1,
            t2.lang as lang2,
            t1.author_id AS author1,
            t2.author_id AS author2,
            t1.created_at AS time1,
            t2.created_at AS time2,
            abs(julianday(t1.created_at) - julianday(t2.created_at)) * 86400 AS seconds_diff
        FROM tweet_urls t1
        JOIN tweet_urls t2 ON
            t1.url = t2.url AND
            t1.id < t2.id AND
            t1.author_id < t2.author_id AND
            t1.lang = t2.lang AND
            t1.possibly_sensitive = t2.possibly_sensitive
        WHERE
            abs(julianday(t1.created_at) - julianday(t2.created_at)) * 86400 <= ?
    """,
        [seconds_between],
    )
    rows = res.fetchall()
    cur.execute("DROP TABLE tweet_urls")
    print(f"Found {rows} entries")
    df = pd.DataFrame(rows)
    if save_csv:
        df.to_csv(f"df_url_connections_s{seconds_between}.csv")

    return df


def common_urls_as_dataframe(
    db: Connection, seconds_between: int, save_csv: bool = False
):
    cur = db.cursor()

    cur.execute("""
        CREATE TEMP TABLE tweet_urls AS
        SELECT
            tweets.id,
            tweets.text,
            tweets.author_id,
            json_extract(value, '$.expanded_url') AS url,
            tweets.lang,
            datetime(created_at) AS created_at
        FROM tweets,
            json_each(json_extract(entities, '$.urls'))
        WHERE
            json_extract(entities, '$.urls') IS NOT NULL
        AND text NOT LIKE 'RT @%'
    """)

    # Create indexes for speed
    cur.execute("CREATE INDEX temp.idx_tweet_urls_url ON tweet_urls(url)")
    cur.execute("CREATE INDEX temp.idx_tweet_urls_id ON tweet_urls(id)")
    cur.execute("CREATE INDEX temp.idx_tweet_urls_author ON tweet_urls(author_id)")
    cur.execute(
        "CREATE INDEX temp.idx_tweet_urls_combined ON tweet_urls(url, id, author_id)"
    )

    res = cur.execute(
        """
        SELECT
            t1.id AS id1,
            t2.id AS id2,
            t1.url,
            t1.text AS text1,
            t2.text AS text2,
            t1.lang as lang1,
            t2.lang as lang2,
            t1.author_id AS author1,
            t2.author_id AS author2,
            t1.created_at AS time1,
            t2.created_at AS time2,
            abs(julianday(t1.created_at) - julianday(t2.created_at)) * 86400 AS seconds_diff
        FROM tweet_urls t1
        JOIN tweet_urls t2 ON
            t1.url = t2.url AND
            t1.id < t2.id AND
            t1.author_id < t2.author_id
        WHERE
            abs(julianday(t1.created_at) - julianday(t2.created_at)) * 86400 <= ?
    """,
        [seconds_between],
    )
    rows = res.fetchall()
    cur.execute("DROP TABLE tweet_urls")
    print(f"Found {rows} entries")
    df = pd.DataFrame(rows)
    if save_csv:
        df.to_csv(f"df_url_connections_s{seconds_between}.csv")

    return df


def parse_referenced_tweets_to_dataframe(row: pd.Series):
    action = row["referenced_tweets"]
    if isinstance(action, float):
        return None
    try:
        if isinstance(action, list) and action:
            nested_df = pd.DataFrame(action)
            return nested_df
    except (ValueError, SyntaxError):
        print(f"Warning: Failed to parse {row}")
        return None
