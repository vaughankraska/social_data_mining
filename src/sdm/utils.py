import pandas as pd
import re
import json


def tweets_as_dataframe(file_path: str = "data/tweets.dat", save=False) -> pd.DataFrame:
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

        if save:
            tweets_df.to_csv("data/tweets.csv", index=False)

        return tweets_df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise
    except Exception as e:
        print("Error in tweets_as_dataframe: ", e)


def clean_tweet(tweet: str) -> str:
    """
    Clean a tweet by removing Twitter-specific formatting elements.
    This is made for the embeddings comparisons between reddit and twitter.
    
    Example:
    >>> clean_tweet("RT @User: Hello #world https://t.co/link")
    'Hello'
    """
    # Remove RT
    tweet = re.sub(r'^RT\s+', '', tweet)
    # Remove @mentions
    tweet = re.sub(r'@\w+:?\s*', '', tweet)
    # Remove hashtags and their text
    tweet = re.sub(r'#\w+\s*', '', tweet)
    # Remove URLs
    tweet = re.sub(r'https?://\S+', '', tweet)
    # Remove trailing ellipsis
    tweet = re.sub(r'…$', '', tweet)
    # Remove extra whitespace
    tweet = re.sub(r'\s+', ' ', tweet)
    # Strip leading/trailing whitespace
    tweet = tweet.strip()

    return tweet
