import os
from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("neo4j", "password")
# Path to the JSON file
JSON_FILE_PATH = "tweets.dat"

# Neo4j connection
driver = GraphDatabase.driver(URI, auth=(AUTH[0], AUTH[1]))


def load_json_to_neo4j():
    with driver.session() as session:
        result = session.run(
            """
            CALL apoc.load.json($file_path)
            YIELD value
            RETURN value
            """,
            {
                "file_path": (JSON_FILE_PATH)
            }
        )

        for record in result:
            # Process the loaded JSON data
            print(record["value"])


if __name__ == "__main__":
    load_json_to_neo4j()
