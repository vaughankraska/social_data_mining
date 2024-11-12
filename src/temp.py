import os
from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("neo4j", "password")
# Path to the JSON file
JSON_FILE_PATH = "tweets.dat"


def query_database():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    session = driver.session(database="neo4j")
    records, summary, keys = driver.execute_query(
        "MATCH (p:tweets) RETURN p.id AS id",
        database_="neo4j",
    )

    # Loop through results and do something with them
    for record in records:
        print(record.data())  # obtain record as dict

    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))
    session.close()
    driver.close()


if __name__ == "__main__":
    query_database()
