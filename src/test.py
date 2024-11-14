from src.config import db_driver
from src.crud import get_tweets_count

with db_driver.session() as session:
    retweeted_tweets = session.execute_read(get_tweets_count)
    for tweet in retweeted_tweets:
        print(tweet)
