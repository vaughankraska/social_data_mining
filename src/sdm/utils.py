import pandas as pd
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
