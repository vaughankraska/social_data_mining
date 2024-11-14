from src.utils import tweets_as_dataframe

df = tweets_as_dataframe("data/tweets_small.dat")
df.to_csv("data/tweets_small.csv", index=False)
