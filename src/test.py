from src.config import db_driver
import pandas as pd
from src.crud import get_tweets_count, get_retweeted_edge_list

with db_driver.session() as session:
    retweeted_tweets = session.execute_read(get_tweets_count)
    for tweet in retweeted_tweets:
        print(tweet)
    retweeted_tweets = session.execute_read(get_retweeted_edge_list)
    nodes_df = pd.DataFrame(retweeted_tweets[0]["graph_data"]["nodes"])
    edges_df = pd.DataFrame(retweeted_tweets[0]["graph_data"]["edges"])
    print("nodes head:")
    print(nodes_df.head())
    print("edges head:")
    print(edges_df.head())
