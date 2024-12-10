import math
from sqlite3 import Connection
import pandas as pd
from typing import Dict, List, Tuple
from text_mining.data import load_sentiment_dict, get_tweet_corpora
from text_mining.language import Language
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
nltk.download("punkt_tab")
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
    tweets: List[str], labels: List[float], test_size: float = 0.20
) -> Tuple[MultinomialNB, CountVectorizer]:
    """
    Trains classifier using MultiNomialNB.

    Example usage from Text analysis lab:
        ```python
        cls_final, vectorizer = train_classifier(
            df["TEXT"].tolist(), labels=df["CODE"], test_size=0.02
        )
        processed_data = ml_annotations = cls_final.predict(
            vectorizer.transform(preprocess_tweets(df["TEXT"]))
        )
        df["ml_sentiment_final"] = ml_annotations
        ```
    """

    preprocessed_tweets = preprocess_tweets(tweets)

    assert len(preprocessed_tweets) == len(labels), "Mismatch labels and data len."

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(preprocessed_tweets)

    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=test_size, random_state=42
    )

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Classification Rep:")
    print(classification_report(y_test, y_pred))

    return clf, vectorizer


def krippendorff_analysis(
    annotations_matrix: np.ndarray, method_names: List[str]
) -> None:
    """
    Calculate and print a summary of Krippendorff's Alpha comparing multiple sentiment analysis methods.
    """
    annotations_matrix = np.array(annotations_matrix)

    assert annotations_matrix.shape[1] == len(
        method_names
    ), "Number of methods must match the number of columns in matrix."

    alpha = krippendorff.alpha(
        reliability_data=annotations_matrix.T, level_of_measurement="ordinal"
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
                agreement = np.mean(
                    annotations_matrix[:, i] == annotations_matrix[:, j]
                )
                print(
                    f"  '{target_method}' vs. '{comparison_method}': {agreement * 100:.2f}% agreement"
                )


def analyze_with_transformer(texts: List[str]) -> List[float]:
    """
    Uses a DistilBERT model fine-tuned on sentiment analysis.
    Does not work with pd.Series! Use text_column.tolist()

    Returns: List[float]: A list of sentiment scores [-1 to 1]
    """

    sentiment_analyzer = pipeline(
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )
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


# Data Driven Utils vvv
def tokenize_corpus(text: str, language: Language = Language.en) -> List[str]:
    """
    Basic wrapper for nltk `word_tokenize`. Note the language param.
    (this is literally just to make sure the downloads at the top of this file
     are properly downloaded)
    """
    return nltk.word_tokenize(text, language=language.to_string())


def remove_stopwords(
        tokens: List[str],
        language: Language
        ) -> Tuple[List[str], set]:
    """Removes stop words.
    Usage:
        >>> from text_mining.language import Language
        >>> from text_mining.utils import tokenize_corpus, remove_stopwords
        >>> tokens = tokenize_corpus("I am a dissapointed developer")
        >>> remove_stopwords(tokens, [Language.en] * len(tokens))
        (['dissapointed', 'developer'], {'doesn', 'wasn', ..., 'in', "don't"})
    """
    try:
        stop_words = set(stopwords.words(language.to_string()))
    except Exception as e:
        print(f"WARNING: Parse failed with lanuage '{language.to_string()}', falling back to english\nErr: {e}")
        stop_words = set(stopwords.words(language="english"))

    # Gotta remove some extra words
    stop_words.update(["https", "rt", "la", "le", "les", "et", "en", "des"])

    return [word.lower() for word in tokens if word.lower() not in stop_words], stop_words


def lemmatize_tokens(
        tokens: List[str],
        language: Language = Language.en
        ) -> List[str]:
    raise NotImplementedError


def remove_non_alphabetic(tokens: List[str]) -> List[str]:
    """
    Removes tokens that contain non-alphabetic characters
    e.g., punctuation, numbers. Might also remove other language's
    characters. Havent tested.
    """
    return [word for word in tokens if word.isalpha()]


def get_preprocessed_LDA(db: Connection, min_chars: int) -> pd.DataFrame:
    """
    db tweets corpora ->
        dataframe ->
            tokenize ->
                remove stop words ->
                    remove non-alpha =>
                        DataFrame with "processed_corpus" col
    Returns a new dataframe with pre-processed text.
    """
    df = get_tweet_corpora(db, min_chars=min_chars)
    langs: List[Language] = df["lang"].apply(
            lambda lang: Language.from_string(lang)
            if lang is not None else Language.en
            )
    corpora: List[str] = df["text_corpus"].tolist()
    assert len(langs) == len(corpora)

    tokens_list = [
            tokenize_corpus(
                corpus,
                language=lang
                ) for corpus, lang in zip(corpora, langs)
            ]
    tokens_list = [
            remove_stopwords(
                tokens,
                language=lang
                )[0] for tokens, lang in zip(tokens_list, langs)
            ]
    tokens_list = [remove_non_alphabetic(tokens) for tokens in tokens_list]

    df["processed_corpus"] = [" ".join(t) for t in tokens_list]

    return df
