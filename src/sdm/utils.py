import re
import json

import pandas as pd

from sdm.config import Connection


def tweets_as_dataframe(file_path: str = "data/tweets.dat", save=False) -> pd.DataFrame:
    data = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    tweet = json.loads(line.strip())
                    data.append(tweet)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
        tweets_df = pd.DataFrame(data)

        if save:
            tweets_df.to_csv("data/tweets.csv", index=False)

        return tweets_df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise
    except Exception as e:
        print("Error in tweets_as_dataframe: ", e)


def clean_text(text: str) -> str:
    """
    Clean a tweet or reddit text by removing Twitter-specific formatting elements.
    This is made for the embeddings comparisons between reddit and twitter.

    Example:
    >>> clean_tweet("RT @User: Hello #world https://t.co/link")
    'Hello'
    """
    # Remove RT
    text = re.sub(r'^RT\s+', '', text)
    # Remove @mentions
    text = re.sub(r'@\w+:?\s*', '', text)
    # Remove hashtags and their text
    text = re.sub(r'#\w+\s*', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove trailing ellipsis
    text = re.sub(r'…$', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()

    return text
        

def get_pi_ba_dataframe(db: Connection) -> pd.DataFrame:
    cur = db.cursor()
    res = cur.execute("""
        SELECT
            a.author_id AS account_id,
            t.id AS doc_id,
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
            (a.lang = 'en' OR a.lang = 'fr')
            AND a.account_type IN ('Private individuals', 'Business actors')                  
    """).fetchall()
    
    return pd.DataFrame(res)

def get_ja_aa_pa_sa_bot_dataframe(db: Connection) -> pd.DataFrame:
    cur = db.cursor()
    res = cur.execute("""
        SELECT
            a.author_id AS account_id,
            t.id AS doc_id,
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
            (a.lang = 'en' OR a.lang = 'fr')
            AND a.account_type IN ('Advocacy actors', 'Journalistic actors', 'Political actors', 'Scientific actors', 'Bots')
    """).fetchall()
    
    return pd.DataFrame(res)