import math
from typing import Dict, List, Tuple
from text_mining.data import load_sentiment_dict
import re
import krippendorff
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from transformers import pipeline

# Gotta download the nltk datasets
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

def annotate_tweet(text: str, sentiment_dict: Dict[str, int]) -> float:
    words = re.findall(r"\b\w+\b", text.lower())
    unique_words = set(words)
    sentiment_score = sum(sentiment_dict.get(word, 0) for word in unique_words)
    word_count = sum(1 for word in unique_words if word in sentiment_dict)

    if word_count == 0:
        return 0

    score = sentiment_score / word_count
    if math.isnan(score):
        return 0
    else:
        return score


def annotate_texts(texts: List[str], sentiment_dict_path: str) -> List[int]:
    sentiment_dict = load_sentiment_dict(sentiment_dict_path)

    return [annotate_tweet(text, sentiment_dict) for text in texts]


def analyze_with_vader(texts: List[str]) -> List[float]:
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = []
    for text in texts:
        score = analyzer.polarity_scores(text.lower())
        vader_scores.append(score["compound"])

    return vader_scores


def preprocess_tweet(text: str) -> str:
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    words = re.findall(r"\b\w+\b", text.lower())

    cleaned_words = [
        lemmatizer.lemmatize(word) for word in words if word not in stop_words
    ]

    return " ".join(cleaned_words)


def preprocess_tweets(texts: List[str]) -> List[str]:
    return [preprocess_tweet(text) for text in texts]


def train_classifier(
    tweets: List[str], labels: List[float]
) -> Tuple[MultinomialNB, CountVectorizer]:

    preprocessed_tweets = preprocess_tweets(tweets)

    assert len(preprocessed_tweets) == len(labels), "Mismatch labels and data len."

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(preprocessed_tweets)

    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Classification Rep:")
    print(classification_report(y_test, y_pred))

    return clf, vectorizer


def krippendorff_analysis(annotations_matrix: np.ndarray, method_names: List[str]) -> None:
    """
    Calculate and print a summary of Krippendorff's Alpha comparing multiple sentiment analysis methods.
    """
    annotations_matrix = np.array(annotations_matrix)

    assert annotations_matrix.shape[1] == len(method_names), \
        "Number of methods must match the number of columns in matrix."

    alpha = krippendorff.alpha(
            reliability_data=annotations_matrix.T,
            level_of_measurement="ordinal"
            )
    print(f"Krippendorff's Alpha: {alpha:.4f}")

    # alpha close to 1, it indicates strong agreement between methods
    if alpha > 0.8:
        print("The methods show strong agreement.")
    elif alpha > 0.6:
        print("The methods show moderate agreement.")
    elif alpha > 0.4:
        print("The methods show weak agreement.")
    else:
        print("The methods show poor agreement.")
    # Summary of agreement between methods
    print("\nMethod-wise Agreement Summary:")
    for i, target_method in enumerate(method_names):
        print(f"\n{target_method} comparison with other methods:")
        for j, comparison_method in enumerate(method_names):
            if i != j:
                agreement = np.mean(annotations_matrix[:, i] == annotations_matrix[:, j])
                print(f"  '{target_method}' vs. '{comparison_method}': {agreement * 100:.2f}% agreement")


def analyze_with_transformer(texts: List[str]) -> List[float]:
    """
    Uses a DistilBERT model fine-tuned on sentiment analysis.
    Does not work with pd.Series! Use text_column.tolist()

    Returns: List[float]: A list of sentiment scores [-1 to 1]
    """

    sentiment_analyzer = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    results = sentiment_analyzer(texts)

    sentiment_scores = []
    for res in results:
        label = res["label"]
        score = res["score"]

        if label == "NEGATIVE":
            sentiment_scores.append(-score)
        else:
            sentiment_scores.append(score)

    return sentiment_scores
