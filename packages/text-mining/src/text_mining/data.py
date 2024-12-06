from sqlite3 import Connection
import pandas as pd

def get_research_dataframe(db: Connection) -> pd.DataFrame:
    cur = db.cursor()
    res = cur.execute("""
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

    return pd.DataFrame(res)
