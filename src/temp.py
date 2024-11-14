from neo4j import GraphDatabase
from src.config import db_driver


def ingest_tweets(driver: GraphDatabase):
    json_file_path = "tweets.csv"

    json_file_path = "file:///" + json_file_path
    with driver.session() as session:
        session.run(
            """
            LOAD CSV WITH HEADERS FROM $file_path AS value
            MERGE (t:Tweet {id: value.id})
            SET t += value
            MERGE (u:User {id: value.author_id})
            WITH t, apoc.convert.fromJsonList(value.referenced_tweets) AS ref_tweets, value
            UNWIND ref_tweets AS ref_tweet
            MERGE (rt:Tweet {id: ref_tweet.id})
            MERGE (t)-[:REFERENCES {type: ref_tweet.type}]->(rt)
            RETURN value
            """,
            {"file_path": (json_file_path)},
        )


if __name__ == "__main__":
    ingest_tweets(db_driver)
    print("Done!!!")
