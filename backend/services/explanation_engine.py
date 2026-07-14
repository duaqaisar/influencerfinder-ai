import pandas as pd


class ExplanationEngine:


    @staticmethod
    def confidence_score(row: pd.Series):

        score = 40


        # Activity confidence

        posts = row.get(
            "posts_count",
            0
        )

        if posts > 0:
            score += 20



        # Engagement confidence

        likes = row.get(
            "avg_likes",
            0
        )

        if likes > 0:
            score += 20



        # Relevance confidence

        relevance = row.get(
            "relevance_score",
            0
        )


        if relevance > 0.30:
            score += 10


        if relevance > 0.60:
            score += 10



        return min(
            score,
            100
        )



    @staticmethod
    def selection_reason(
        row: pd.Series,
        topic: str
    ):

        reasons = []



        relevance = row.get(
            "relevance_score",
            0
        )


        if relevance >= 0.80:

            reasons.append(
                f"highly relevant to '{topic}'"
            )


        elif relevance >= 0.50:

            reasons.append(
                f"moderately relevant to '{topic}'"
            )


        else:

            reasons.append(
                f"loosely related to '{topic}'"
            )



        followers = row.get(
            "followers",
            0
        )



        if followers >= 1_000_000:

            reasons.append(
                f"mega influencer with {followers/1_000_000:.1f}M followers"
            )


        elif followers >= 100_000:

            reasons.append(
                f"macro influencer with {followers/1000:.0f}K followers"
            )


        elif followers >= 10_000:

            reasons.append(
                f"micro influencer with {followers/1000:.0f}K followers"
            )



        likes = row.get(
            "avg_likes",
            0
        )


        if likes > 0 and followers > 0:

            engagement = (
                likes
                /
                followers
            ) * 100


            reasons.append(
                f"engagement rate {engagement:.1f}%"
            )



        posts = row.get(
            "posts_count",
            0
        )


        if posts > 0:

            reasons.append(
                f"{int(posts)} posts analyzed"
            )



        return (
            f"@{row.get('username','')} was selected because they are "
            + ", ".join(reasons)
            + "."
        )
