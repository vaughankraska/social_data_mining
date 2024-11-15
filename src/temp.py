from neo4j import GraphDatabase
from src.config import db_driver


def ingest_tweets(driver: GraphDatabase):
    csv_file_path = "tweets.csv"
    batch_size = 10_000
    thread_count = 8

    csv_file_path = "file:///" + csv_file_path
    with driver.session() as session:
        batch_query = """
        CALL apoc.periodic.iterate(
                "LOAD CSV WITH HEADERS FROM $file_path AS value RETURN value",
                "
                MERGE (t:Tweet {id: value.id})
                SET t += value
                MERGE (u:User {id: value.author_id})
                WITH t, apoc.convert.fromJsonList(value.referenced_tweets) AS ref_tweets, value
                UNWIND ref_tweets AS ref_tweet
                MERGE (rt:Tweet {id: ref_tweet.id})
                MERGE (t)-[:REFERENCES {type: ref_tweet.type}]->(rt)
                ",
                {
                    batchSize: $batch_size,
                    parallel: true,
                    concurrency: $thread_count,
                    params: {file_path: $file_path}
                    }
                ) YIELD batches, total, committedOperations, failedOperations, failedBatches, retries, errorMessages, batch, operations
        RETURN batches, total, committedOperations, failedOperations, failedBatches, retries, errorMessages
        """
        result = session.run(
            batch_query,
            {
                "file_path": csv_file_path,
                "batch_size": batch_size,
                "thread_count": thread_count
            }
        )
        for row in result:
            print(row)
        # session.run(
        #     """
        #     LOAD CSV WITH HEADERS FROM $file_path AS value
        #     MERGE (t:Tweet {id: value.id})
        #     SET t += value
        #     MERGE (u:User {id: value.author_id})
        #     WITH t, apoc.convert.fromJsonList(value.referenced_tweets) AS ref_tweets, value
        #     UNWIND ref_tweets AS ref_tweet
        #     MERGE (rt:Tweet {id: ref_tweet.id})
        #     MERGE (t)-[:REFERENCES {type: ref_tweet.type}]->(rt)
        #     RETURN value
        #     """,
        #     {"file_path": (csv_file_path)},
        # )


if __name__ == "__main__":
    ingest_tweets(db_driver)
    print("Done!!!")
