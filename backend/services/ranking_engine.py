import numpy as np
import pandas as pd


class RankingEngine:


    @staticmethod
    def safe_numeric(series):

        return pd.to_numeric(
            series,
            errors="coerce"
        ).fillna(0)



    @staticmethod
    def log_scale(series):

        values = np.log1p(
            RankingEngine.safe_numeric(series)
            .clip(lower=0)
        )

        max_value = values.max()

        if max_value == 0:
            return values

        return values / max_value



    @classmethod
    def calculate_influence(
        cls,
        df: pd.DataFrame
    ):

        """
        Measures social influence.

        Components:

        40% Followers
        35% Engagement
        25% Activity
        """


        followers = cls.safe_numeric(
            df.get(
                "followers",
                0
            )
        )


        likes = cls.safe_numeric(
            df.get(
                "avg_likes",
                0
            )
        )


        posts = cls.safe_numeric(
            df.get(
                "posts_count",
                0
            )
        )


        follower_score = (
            cls.log_scale(followers)
            *
            0.40
        )


        engagement_rate = (
            likes /
            followers.replace(
                0,
                np.nan
            )
        ).fillna(0)


        engagement_score = (
            cls.log_scale(
                engagement_rate
            )
            *
            0.35
        )


        activity_score = (
            cls.log_scale(posts)
            *
            0.25
        )


        return (
            follower_score
            +
            engagement_score
            +
            activity_score
        ).clip(0,1)



    @staticmethod
    def calculate_expertise(
        df: pd.DataFrame
    ):

        """
        Measures niche expertise.
        """

        keywords = [
            "fitness",
            "gym",
            "workout",
            "training",
            "bodybuilding",
            "exercise",
            "muscle",
            "strength",
            "cardio",
            "nutrition",
            "coach",
            "athlete"
        ]


        scores = []


        for text in df["text"].astype(str):

            text = text.lower()

            hits = sum(
                1
                for k in keywords
                if k in text
            )


            scores.append(
                min(
                    hits / len(keywords),
                    1
                )
            )


        return pd.Series(
            scores,
            index=df.index
        )



    @staticmethod
    def calculate_overall(
        df: pd.DataFrame
    ):

        """
        Final ranking score.

        Relevance is the primary ranking signal.

        Formula:

        Overall =
            75% Semantic Relevance
            25% Social Influence

        Weak relevance gets penalized.
        """


        relevance = pd.to_numeric(
            df.get(
                "relevance_score",
                0
            ),
            errors="coerce"
        ).fillna(0)



        influence = pd.to_numeric(
            df.get(
                "influence_score",
                0
            ),
            errors="coerce"
        ).fillna(0)



        # Main score

        overall = (

            relevance * 0.75

            +

            influence * 0.25

        )



        # Relevance gate
        # Prevent unrelated famous accounts
        # from ranking high

        overall = overall.where(
            relevance >= 0.25,
            overall * 0.20
        )



        return overall.clip(
            0,
            1
        )
