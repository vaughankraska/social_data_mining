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