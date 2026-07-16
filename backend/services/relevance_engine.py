from services.embedding_engine import EmbeddingEngine
from services.embedding_cache import EmbeddingCache

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Computes how relevant each influencer profile is to a given search topic,
# using a combination of keyword matching, semantic embeddings, and TF-IDF
class RelevanceEngine:

    # Predefined keyword sets for common topics, used for fast keyword-based matching
    TOPIC_KEYWORDS = {


        "fitness": [

            "fitness",
            "gym",
            "workout",
            "workouts",
            "training",
            "bodybuilding",
            "bodybuilder",
            "exercise",
            "muscle",
            "strength",
            "cardio",
            "yoga",
            "nutrition",
            "diet",
            "protein",
            "coach",
            "trainer",
            "athlete",
            "physique",
            "weightlifting",
            "crossfit"

        ],



        "beauty": [

            "beauty",
            "makeup",
            "skincare",
            "cosmetics",
            "hair",
            "fashion",
            "style",
            "glow",
            "lifestyle"

        ],



        "fashion": [

            "fashion",
            "style",
            "clothing",
            "outfit",
            "designer",
            "model",
            "luxury",
            "streetwear"

        ],



        "sports": [

            "sports",
            "football",
            "cricket",
            "basketball",
            "athlete",
            "player",
            "team",
            "training"

        ],



        "technology": [

            "technology",
            "coding",
            "software",
            "developer",
            "programming",
            "ai",
            "machine learning",
            "data",
            "computer"

        ]

    }




    @classmethod
    def get_keywords(
        cls,
        topic
    ):

        # Normalize the topic string (lowercase, trimmed)
        topic = (
            str(topic)
            .lower()
            .strip()
        )

        # If the topic matches a predefined category, use its keyword list
        if topic in cls.TOPIC_KEYWORDS:

            return cls.TOPIC_KEYWORDS[topic]

        # Otherwise, fall back to splitting the topic string into individual words as keywords
        return topic.split()





    @staticmethod
    def normalize(
        series
    ):

        # Min-max normalize a series to a 0-1 range
        minimum = series.min()

        maximum = series.max()

        # Avoid division by zero if all values are the same
        if maximum == minimum:

            return pd.Series(
                [0] * len(series),
                index=series.index
            )


        return (
            series - minimum
        ) / (
            maximum - minimum
        )






    @classmethod
    def keyword_score(
        cls,
        texts,
        keywords
    ):

        # Score each text based on how many of the given keywords it contains
        scores = []


        for text in texts.fillna("").astype(str):


            text = text.lower()


            # Count how many keywords appear in this text
            hits = sum(

                1

                for keyword in keywords

                if keyword.lower() in text

            )


            # Score as fraction of total keywords matched
            score = (

                hits /

                len(keywords)

            )


            # Cap the score at 1 (safety, though it shouldn't normally exceed it)
            scores.append(

                min(
                    score,
                    1
                )

            )



        return pd.Series(

            scores,

            index=texts.index

        )







    @classmethod
    def semantic_score(
        cls,
        texts,
        topic
    ):

        # Score each text based on semantic (embedding) similarity to the topic
        try:

            # Make sure embeddings are built/loaded before searching
            EmbeddingCache.ensure_ready()


            # Encode the topic string into an embedding vector
            query_embedding = (

                EmbeddingEngine
                .encode(
                    [
                        topic
                    ]
                )[0]

            )


            # Compute similarity between the topic embedding and all cached profile embeddings
            scores = (

                EmbeddingEngine
                .similarity(
                    query_embedding,
                    EmbeddingCache.embeddings
                )

            )


            # Align scores with the texts' index, truncating to match length
            scores = pd.Series(

                scores[:len(texts)],

                index=texts.index

            )


            # Normalize scores to a 0-1 range
            return cls.normalize(
                scores
            )



        except Exception as e:

            # If semantic scoring fails for any reason, log the error and return all zeros
            print(
                "[Semantic Error]",
                e
            )



            return pd.Series(

                [0] * len(texts),

                index=texts.index

            )







    @classmethod
    def tfidf_score(
        cls,
        texts,
        topic
    ):

        # Score each text based on TF-IDF cosine similarity to the topic
        try:

            # Build a text corpus from all profile texts
            corpus = (

                texts
                .fillna("")
                .astype(str)
                .tolist()

            )


            # Configure a TF-IDF vectorizer using unigrams and bigrams, ignoring English stopwords
            vectorizer = TfidfVectorizer(

                stop_words="english",

                ngram_range=(1,2)

            )


            # Fit the vectorizer on the corpus plus the topic (appended as the last "document")
            matrix = (

                vectorizer
                .fit_transform(

                    corpus + [topic]

                )

            )


            # The last row of the matrix corresponds to the topic's vector
            query_vector = matrix[-1]


            # Compute cosine similarity between the topic vector and all profile vectors
            scores = (

                cosine_similarity(

                    query_vector,

                    matrix[:-1]

                )[0]

            )



            return pd.Series(

                scores,

                index=texts.index

            )



        except Exception:

            # If TF-IDF scoring fails for any reason, return all zeros
            return pd.Series(

                [0] * len(texts),

                index=texts.index

            )








    @classmethod
    def hybrid_relevance(
        cls,
        text_series,
        topic
    ):

        # Get the keyword list for this topic
        keywords = (

            cls.get_keywords(
                topic
            )

        )


        # Compute raw keyword-based score
        keyword = (

            cls.keyword_score(

                text_series,

                keywords

            )

        )

        # Normalize keyword score to 0-1 range so its weight is
        # comparable to semantic/tfidf. Without this, keyword's real
        # max is ~1/len(keywords), so its 0.40 weight barely matters.
        keyword = cls.normalize(keyword)


        # Compute semantic (embedding-based) score
        semantic = (

            cls.semantic_score(

                text_series,

                topic

            )

        )


        # Compute TF-IDF based score
        tfidf = (

            cls.tfidf_score(

                text_series,

                topic

            )

        )

        # Normalize tfidf for the same reason as keyword above.
        tfidf = cls.normalize(tfidf)




        # Final relevance score
        # Keyword matching is stronger to avoid unrelated influencers
        # Weighted combination of all three scoring methods
        relevance = (

            semantic * 0.45

            +

            keyword * 0.40

            +

            tfidf * 0.15

        )

        # Suppress relevance for profiles with zero keyword hits.
        # Semantic similarity alone is noisy on short text (bios/names)
        # and shouldn't be able to carry an unrelated profile to the top
        # just because normalization stretched its score toward 1.0.
        relevance = relevance.where(
            keyword > 0,
            relevance * 0.15
        )

        # Return final clipped relevance scores along with the keyword list used
        return (

            relevance.clip(
                0,
                1
            ),

            keywords

        )







    @classmethod
    def keyword_relevance(
        cls,
        text_series,
        topic
    ):

        # Simpler relevance calculation based purely on keyword matching (no semantic/tfidf)
        keywords = (

            cls.get_keywords(
                topic
            )

        )


        scores = (

            cls.keyword_score(

                text_series,

                keywords

            )

        )



        return (

            scores,

            keywords

        )
