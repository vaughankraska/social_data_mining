from src.config import db_driver
from src.crud import get_retweeted_tweets, get_tweets_with_geo

with db_driver.session() as session:
    retweeted_tweets = session.execute_read(get_tweets_with_geo)
    for tweet in retweeted_tweets:
        print(tweet)
