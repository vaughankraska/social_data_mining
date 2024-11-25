from src.config import get_db_connection
from src.utils import common_urls_as_dataframe


def main(seconds_between: int):
    db = get_db_connection()

    df = common_urls_as_dataframe(db=db, seconds_between=seconds_between)
    print(df.head())
    df.to_csv(f"data/df_url_connections_s{seconds_between}.csv")

# def main(seconds_between: int):
#     db = get_db_connection()
#     cur = db.cursor()

#     res = cur.execute("""
#         WITH tweet_urls AS (
#             SELECT
#                 tweets.id,
#                 tweets.text,
#                 tweets.author_id,
#                 json_extract(value, '$.expanded_url') AS url,
#                 tweets.lang,
#                 datetime(created_at) AS created_at
#             FROM tweets,
#                 json_each(json_extract(entities, '$.urls'))
#             WHERE
#                 json_extract(entities, '$.urls') IS NOT NULL
#         )
#         SELECT
#             t1.id AS id1,
#             t2.id AS id2,
#             t1.url,
#             t1.text AS text1,
#             t2.text AS text2,
#             t1.author_id AS author1,
#             t2.author_id AS author2,
#             t1.created_at AS time1,
#             t2.created_at AS time2,
#             abs(julianday(t1.created_at) - julianday(t2.created_at)) * 86400 AS seconds_diff
#         FROM tweet_urls t1
#         JOIN tweet_urls t2 ON
#             t1.url = t2.url AND
#             t1.id != t2.id AND
#             t1.author_id != t2.author_id
#         WHERE
#             seconds_diff <= ?
#     """, [seconds_between])
#     rows = res.fetchall()
#     print(rows)
#     print(len(rows))


# def main(seconds_between: int):
#     db = get_db_connection()
#     cur = db.cursor()

#     res = cur.execute("""
#             SELECT
#                 tweets.id,
#                 tweets.author_id,
#                 json_extract(value, '$.expanded_url') AS url,
#                 tweets.lang,
#                 datetime(created_at) AS created_at
#             FROM tweets,
#                 json_each(json_extract(entities, '$.urls'))
#             WHERE
#                 json_extract(entities, '$.urls') IS NOT NULL
#                 """)
#     print(len(res.fetchall()))


if __name__ == "__main__":
    main(1)
