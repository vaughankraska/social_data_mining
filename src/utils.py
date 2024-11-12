import json
import pandas as pd
from neo4j import GraphDatabase


def tweets_as_dataframe(file_path: str = "data/tweets.dat"):
    data = []

    try:
        with open(file_path, 'r') as file:
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


def load_json_to_neo4j(
        uri: str = "neo4j://localhost",
        auth: tuple = ("neo4j", "password"),
        json_file_path: str = "tweets.dat"
        ):
    driver = GraphDatabase.driver(uri, auth=auth)
    with driver.session() as session:
        result = session.run(
            """
            CALL apoc.load.json($file_path)
            YIELD value
            RETURN value
            """,
            {
                "file_path": (json_file_path)
            }
        )

        for record in result:
            # Process the loaded JSON data
            print(record["value"])
