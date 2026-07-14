from services.embedding_engine import EmbeddingEngine
from services.embedding_cache import EmbeddingCache

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



class RelevanceEngine:


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


        topic = (
            str(topic)
            .lower()
            .strip()
        )


        if topic in cls.TOPIC_KEYWORDS:

            return cls.TOPIC_KEYWORDS[topic]


        return topic.split()





    @staticmethod
    def normalize(
        series
    ):


        minimum = series.min()

        maximum = series.max()


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


        scores = []


        for text in texts.fillna("").astype(str):


            text = text.lower()



            hits = sum(

                1

                for keyword in keywords

                if keyword.lower() in text

            )



            score = (

                hits /

                len(keywords)

            )



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


        try:


            EmbeddingCache.ensure_ready()



            query_embedding = (

                EmbeddingEngine
                .encode(
                    [
                        topic
                    ]
                )[0]

            )



            scores = (

                EmbeddingEngine
                .similarity(
                    query_embedding,
                    EmbeddingCache.embeddings
                )

            )



            scores = pd.Series(

                scores[:len(texts)],

                index=texts.index

            )



            return cls.normalize(
                scores
            )



        except Exception as e:


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


        try:


            corpus = (

                texts
                .fillna("")
                .astype(str)
                .tolist()

            )



            vectorizer = TfidfVectorizer(

                stop_words="english",

                ngram_range=(1,2)

            )



            matrix = (

                vectorizer
                .fit_transform(

                    corpus + [topic]

                )

            )



            query_vector = matrix[-1]



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



        keywords = (

            cls.get_keywords(
                topic
            )

        )



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



        semantic = (

            cls.semantic_score(

                text_series,

                topic

            )

        )



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
