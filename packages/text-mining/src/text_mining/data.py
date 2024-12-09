from typing import Dict
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


def load_sentiment_dict(file_path: str = "data/COPSSentimentDict.csv") -> Dict:
    df = pd.read_csv(file_path, delimiter=";")
    df = df.drop_duplicates(subset="TERM", keep="first")
    sentiment_dict = pd.Series(
        df["SENTIMENT"].values, index=df["TERM"].str.lower()
    ).to_dict()

    return sentiment_dict


def load_excel_annotations(file_path: str) -> pd.DataFrame:
    """Ex: file_path = "data/train.xlsx" """
    excel_data = pd.ExcelFile(file_path)
    sheet_names = ['INSTRUCTIONS', 'CODER1', 'CODER2', 'CODER3']
    assert len(excel_data.sheet_names) == 4, "Sheets mismatch in excel file"
    assert sheet_names == excel_data.sheet_names, "Sheet names mismatch expectations"
    coder1_df = pd.read_excel(file_path, sheet_name=sheet_names[1])
    coder1_df["coder"] = 1

    return coder1_df
