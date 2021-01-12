import numpy as np
import pandas as pd
import re
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics.pairwise import cosine_similarity
import src.constants as const

nltk.download('punkt')

stemmer = nltk.stem.snowball.SnowballStemmer("english", ignore_stopwords=False)
pipe_ifidfmatrix = [('counter_vectorizer',
                     CountVectorizer(max_features=200000, ngram_range=(1, 3))),
                    ('tfidf_transform', TfidfTransformer())]


def normalize_text(text, stemmer=stemmer):
    """
        tokenize and normalize a string of text to it's word stem (e.x. analyzing -> analyz)
    """
    sentences = nltk.sent_tokenize(text)

    words = []
    for sent in sentences:
        words.extend(nltk.word_tokenize(sent))

    stems = [stemmer.stem(w) for w in words if re.match('[a-zA-Z]+', w)]
    normalized_text = ' '.join(stems)

    return normalized_text


def normalized_description(list_of_descriptions):
    """
        tokenize and normalize descriptions for images
    """
    normalized_tokens = [normalize_text(desc) for desc in list_of_descriptions]
    return normalized_tokens


def normalized_tags(list_of_tags):
    """
        tokenize and normalize tags for images
    """
    normalized_tokens = [
        ' '.join([normalize_text(tag) for tag in tags])
        for tags in list_of_tags
    ]
    return normalized_tokens


def nlp_normalize(col):
    """
        choose which normalize function to include in sklearn pipeline - depend if it is for tags or description
    """
    if col == 'description':
        return [('normalize',
                 FunctionTransformer(normalized_description, validate=False))]
    elif col == 'tags':
        return [('normalize',
                 FunctionTransformer(normalized_tags, validate=False))]


def nlp_similarity(data, col, index=-1):
    """
        call sklearn pipeline and fit TI-IDF matrix into NLP model for image text similarity
    """
    pipe = nlp_normalize(col) + pipe_ifidfmatrix
    pipeline = Pipeline(pipe)

    tfidf_matrix = pipeline.fit_transform(data)

    similarity_distance = cosine_similarity(tfidf_matrix)
    similarity_vector = similarity_distance[index]

    return similarity_vector


def similarity(df, description):
    """
        compute similarity score for image search -- bag of words technique
    """
    df_row = pd.DataFrame({
        'description': description,
        'tags': [[description]]
    })
    df = df.append(df_row)
    cols = list(df.columns)

    df['similarity_description'] = nlp_similarity(df['description'].to_list(),
                                                  'description')
    df['similarity_tags'] = nlp_similarity(df['tags'].to_list(), 'tags')
    df[const.SIMILARCOL_] = [
        max(x, y)
        for x, y in zip(df['similarity_description'], df['similarity_tags'])
    ]

    df = df.dropna(subset=['idd'])
    df = df[df[const.SIMILARCOL_] > 0].sort_values(by=[const.SIMILARCOL_],
                                                   ascending=[False])
    df[const.SIMILARCOL_] = df[const.SIMILARCOL_].apply(
        lambda x: f'{round(x*100, 2)}%')

    return df[cols + [const.SIMILARCOL_]]
