from nltk.stem import WordNetLemmatizer
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import nltk

nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words("english")


def lower_text(text):
    return text.lower()


def remove_stopwords(text):
    tokens = [word for word in text.split() if word not in stopwords]
    return " ".join(tokens)


def remove_punctuation(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def remove_whitespace(text):
    return re.sub(" +", " ", text)


def lemmatize(text):
    tokens = [lemmatizer.lemmatize(word) for word in text.split()]
    return " ".join(tokens)


def preprocess(text):
    text = lower_text(text)
    # text = remove_stopwords(text)
    text = remove_punctuation(text)
    text = lemmatize(text)
    text = remove_whitespace(text)
    return text


def count_frequency(documents, threshold=0.2):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    tfidf_values = X.toarray()
    filtered_words = np.array(feature_names)[
        np.where(np.mean(tfidf_values, axis=0) < threshold)
    ]

    return filtered_words


def vectorize_diary(diary):
    def filter(text):
        tokens = [word for word in text.split() if word in filtered_words]
        return " ".join(tokens)

    diary = diary["data"]["diaries"]
    documents = [entry["content"] for entry in diary]

    df = pd.DataFrame(documents, columns=["content"])
    df["content"] = df["content"].apply(preprocess)
    filtered_words = count_frequency(list(df["content"].values))
    df["content"] = df["content"].apply(filter)
    return df
