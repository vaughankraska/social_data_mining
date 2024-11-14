from neo4j import GraphDatabase
from src.config import db_driver


def ingest_tweets(driver: GraphDatabase):
    # load_tweet_json_to_neo4j(driver)
    json_file_path = "tweets.dat"
    with driver.session() as session:
        result = session.run(
            """
            CALL apoc.load.json($file_path)
            YIELD value
            MERGE (t:Tweet {id: value.id})
            SET t += value
            MERGE (u:User {id: value.author_id})
            WITH t, value
            UNWIND value.referenced_tweets AS ref_tweet
            MERGE (rt:Tweet {id: ref_tweet.id})
            MERGE (t)-[:REFERENCES {type: ref_tweet.type}]->(rt)
            RETURN value
            """,
            {"file_path": (json_file_path)},
        )

        print(len(result))
        print("Done!")


if __name__ == "__main__":
    ingest_tweets(db_driver)
