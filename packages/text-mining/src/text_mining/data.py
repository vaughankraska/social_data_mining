import os
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
    """
    Ex: file_path = "data/train.xlsx"
    Note! You should also have the gpt.tsv file in the data/ dir.
        The gpt.tsv file is on studium in the lab.
    """
    excel_data = pd.ExcelFile(file_path)
    sheet_names = ['INSTRUCTIONS', 'CODER1', 'CODER2', 'CODER3']

    assert len(excel_data.sheet_names) == 4, "Sheets mismatch in excel file"
    assert sheet_names == excel_data.sheet_names, "Sheet names mismatch expectations"

    coder1_df = pd.read_excel(file_path, sheet_name=sheet_names[1])
    coder1_df["coder"] = 1

    data_dir = os.path.dirname(file_path)
    gpt_df = pd.read_csv(os.path.join(data_dir, "gpt.tsv"), delimiter="\t")
    gpt_df.rename(columns={"SENTIMENT": "gpt_sentiment"}, inplace=True)


    merged_df = pd.merge(coder1_df, gpt_df, on="ID", how="left")

    return merged_df
