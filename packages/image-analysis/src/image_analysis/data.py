from sqlite3 import Connection
import pandas as pd
def get_images_dataframe(db: Connection) -> pd.DataFrame:
    cur = db.cursor()
    res = cur.execute("""
        SELECT
            a.author_id AS account_id,
            t.attachments AS image_id,
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
            a.account_type IN ('Private individuals', 'Business actors')                  
    """).fetchall()   # Since it's images, have removed the english filter a.lang = 'en'
    
    return pd.DataFrame(res)