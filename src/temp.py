import json
from neo4j import GraphDatabase
from src.config import db_driver
from src.crud import (
    create_tweet,
    create_references_relationship,
    create_posted_by_relationship,
    create_user,
)


def ingest_tweets(driver: GraphDatabase, tweets_file, accounts_file):
    tweet_count = 0
    account_count = 0
    with driver.session() as session:
        with open(tweets_file, "r") as f:
            for line in f:
                tweet_data: dict = json.loads(line)
                tweet_data.pop("entities", None)
                session.execute_write(create_tweet, tweet_data)
                tweet_count += 1
                if tweet_count % 99 == 0:
                    print(f"[*] tweets inserted: {tweet_count}")

                referenced_tweets = json.loads(tweet_data.get("referenced_tweets"))
                if referenced_tweets:
                    for referenced_tweet in referenced_tweets:
                        session.execute_write(
                            create_references_relationship,
                            tweet_data["id"],
                            referenced_tweet["id"],
                            referenced_tweet["type"],
                        )

                session.execute_write(
                    create_posted_by_relationship,
                    tweet_data["id"],
                    tweet_data["author_id"],
                )

        with open(accounts_file, "r") as f:
            for line in f:
                author_id, type, lang, stance = line.strip().split("\t")
                user_data = {
                    "author_id": author_id,
                    "type": type,
                    "lang": lang,
                    "stance": stance,
                }
                session.execute_write(create_user, user_data)
                account_count += 1
                if account_count % 99 == 0:
                    print(f"[*] users inserted: {account_count}")


if __name__ == "__main__":
    ingest_tweets(db_driver, "data/tweets.dat", "data/accounts.tsv")
