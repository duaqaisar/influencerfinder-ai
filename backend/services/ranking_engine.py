import numpy as np
import pandas as pd

# Handles scoring and ranking logic for influencer relevance/influence
class RankingEngine:

    @staticmethod
    def safe_numeric(series):
        # Convert a series to numeric, turning invalid values into NaN, then fill NaN with 0
        return pd.to_numeric(
            series,
            errors="coerce"
        ).fillna(0)

    @staticmethod
    def log_scale(series):
        # Apply log(1 + x) scaling to reduce the impact of extreme outliers (e.g. huge follower counts)
        values = np.log1p(
            RankingEngine.safe_numeric(series)
            .clip(lower=0)  # Ensure no negative values before log
        )
        max_value = values.max()
        # Avoid division by zero if all values are 0
        if max_value == 0:
            return values
        # Normalize values to a 0-1 range relative to the max
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
        # Extract and clean the relevant numeric columns
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

        # Follower component (40% weight), log-scaled to reduce outlier skew
        follower_score = (
            cls.log_scale(followers)
            *
            0.40
        )

        # Calculate engagement rate (avg likes / followers), avoiding divide-by-zero
        engagement_rate = (
            likes /
            followers.replace(
                0,
                np.nan
            )
        ).fillna(0)
        # Engagement component (35% weight), log-scaled
        engagement_score = (
            cls.log_scale(
                engagement_rate
            )
            *
            0.35
        )

        # Activity component (25% weight), based on post count, log-scaled
        activity_score = (
            cls.log_scale(posts)
            *
            0.25
        )

        # Combine all three weighted components into a final influence score, capped between 0 and 1
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
        # Hardcoded list of fitness-related keywords used to gauge niche expertise
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
        # For each influencer's text, count how many keywords appear
        for text in df["text"].astype(str):
            text = text.lower()
            hits = sum(
                1
                for k in keywords
                if k in text
            )
            # Normalize the hit count into a 0-1 score based on total keyword list size
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
        # Extract and clean relevance and influence scores
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
        # Weighted combination: relevance matters more than raw influence
        overall = (
            relevance * 0.75
            +
            influence * 0.25
        )

        # Relevance gate
        # Prevent unrelated famous accounts
        # from ranking high
        # If relevance is too low, heavily penalize the overall score (reduce to 20%)
        # regardless of how influential the account is
        overall = overall.where(
            relevance >= 0.25,
            overall * 0.20
        )

        # Ensure the final score stays within a 0-1 range
        return overall.clip(
            0,
            1
        )
