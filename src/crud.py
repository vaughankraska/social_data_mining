import json
from neo4j import Session
from typing import Dict, Any


def get_tweets_count(tx: Session):
    result = tx.run("""
        MATCH (t:Tweet)
        RETURN count(t) AS tweet_count;
    """)
    return result.data()

def get_retweeted_tweets(tx: Session):
    result = tx.run("""
        MATCH (t:Tweet)-[r:REFERENCES {type: 'retweet'}]->(rt:Tweet)
        RETURN t, r, rt
    """)
    return result.data()


def get_retweeted_edge_list(tx: Session):
    result = tx.run("""
        MATCH (u:User)
        WITH COLLECT(DISTINCT {
          id: u.id,
          label: 'User',
          properties: {
            author_id: u.id
          }
        }) as nodes

        MATCH (t1:Tweet)-[r:REFERENCES {type: 'retweeted'}]->(t2:Tweet)
        WHERE t1.author_id IS NOT NULL AND t2.author_id IS NOT NULL
        WITH nodes, COLLECT(DISTINCT {
          source: t1.author_id,
          target: t2.author_id,
          type: 'RETWEET',
          weight: 1
        }) as edges

        RETURN {
          nodes: nodes,
          edges: edges
        } as graph_data
                    """)
    return result.data()


def create_tweet(tx: Session, tweet_data: Dict[str, Any]):
    tweet_data['referenced_tweets'] = json.dumps(tweet_data.get('referenced_tweets'))
    tweet_data['context_annotations'] = json.dumps(tweet_data.get('context_annotations'))
    tweet_data['public_metrics'] = json.dumps(tweet_data.get('public_metrics'))
    tweet_data['attachments'] = json.dumps(tweet_data.get('attachments'))
    tweet_data['geo'] = json.dumps(tweet_data.get('geo'))
    tweet_data['withheld'] = json.dumps(tweet_data.get('withheld'))

    tx.run("""
        MERGE (t:Tweet {id: $tweet_data.id})
        SET t += $tweet_data
        RETURN t
    """, tweet_data=tweet_data)


def create_user(tx: Session, user_data: Dict[str, Any]) -> None:
    tx.run(
        """
        CREATE (u:User)
        SET u = $user_data
        RETURN u
    """,
        user_data=user_data,
    )


def create_mentions_relationship(tx: Session, tweet_id: str, user_id: str) -> None:
    tx.run(
        """
        MATCH (t:Tweet), (u:User)
        WHERE t.id = $tweet_id AND u.author_id = $user_id
        CREATE (t)-[:MENTIONS]->(u)
    """,
        tweet_id=tweet_id,
        user_id=user_id,
    )


def create_uses_hashtag_relationship(tx: Session, tweet_id: str, hashtag: str) -> None:
    tx.run(
        """
        MATCH (t:Tweet)
        WHERE t.id = $tweet_id
        CREATE (t)-[:USES_HASHTAG]->(:Hashtag {tag: $hashtag})
    """,
        tweet_id=tweet_id,
        hashtag=hashtag,
    )


def create_uses_url_relationship(tx: Session, tweet_id: str, url: str) -> None:
    tx.run(
        """
        MATCH (t:Tweet)
        WHERE t.id = $tweet_id
        CREATE (t)-[:USES_URL]->(:URL {url: $url})
    """,
        tweet_id=tweet_id,
        url=url,
    )


def create_references_relationship(
    tx: Session, tweet_id: int, referenced_tweet_id: int, referenced_tweet_type: str
):
    tx.run(
        """
        MATCH (t:Tweet), (rt:Tweet)
        WHERE t.id = $tweet_id AND rt.id = $referenced_tweet_id
        CREATE (t)-[:REFERENCES {type: $referenced_tweet_type}]->(rt)
    """,
        tweet_id=tweet_id,
        referenced_tweet_id=referenced_tweet_id,
        referenced_tweet_type=referenced_tweet_type,
    )


def create_posted_by_relationship(tx: Session, tweet_id: str, user_id: str) -> None:
    tx.run(
        """
        MATCH (t:Tweet), (u:User)
        WHERE t.id = $tweet_id AND u.author_id = $user_id
        CREATE (t)-[:POSTED_BY]->(u)
    """,
        tweet_id=tweet_id,
        user_id=user_id,
    )
