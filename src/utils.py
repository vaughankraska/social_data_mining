import json
import pandas as pd
from neo4j import GraphDatabase
from typing import Optional, Any, Dict


def tweets_as_dataframe(file_path: str = "data/tweets.dat"):
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

        return tweets_df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise
    except Exception as e:
        print("Error in tweets_as_dataframe: ", e)


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


def get_entity_or_none(data: Dict[str, Any], key: str) -> Optional[Any]:
    if key in data:
        return data[key]
    return None


def load_tweet_json_to_neo4j(
    driver: GraphDatabase,
    json_file_path: str = "tweets.dat",
):
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

        for record in result:
            # Print the loaded JSON data
            print(record["value"])
