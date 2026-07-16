import pandas as pd
from services.search_pipeline import SearchPipeline

from services.influencer_profile_builder import (
    InfluencerProfileBuilder
)

from services.relevance_engine import (
    RelevanceEngine
)

from services.ranking_engine import (
    RankingEngine
)

from services.explanation_engine import (
    ExplanationEngine
)


# Main service that orchestrates the full influencer search/ranking pipeline
class InfluencerService:

    def find_influencers(
        self,
        topic: str,
        top_n: int = 10,
        platform: str = None
    ):

        # Refresh scraped/search data related to the topic before building profiles
        SearchPipeline.refresh(
            topic=topic,
            limit=max(top_n, 20),
        )

        # Build combined text profiles for all influencers
        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        # Convert profiles into a DataFrame for easier filtering/scoring
        df = pd.DataFrame(
            profiles
        )


        # Platform filtering

        # If a platform filter was provided, keep only matching rows (case-insensitive)
        if platform:

            df = df[
                df["platform"]
                .astype(str)
                .str.lower()
                ==
                platform.lower()
            ]


        # If no influencers remain after filtering, return an empty-result message
        if df.empty:
            return {
                "message": "No influencers found."
            }


        # Cleaning

        # Replace any NaN values with empty strings
        df = df.fillna("")

        # Drop rows with invalid/too-short usernames
        df = df[
            df["username"]
            .astype(str)
            .str.len()
            > 1
        ]


        # Remove duplicate influencers (same username + platform combo)
        df = (
            df
            .drop_duplicates(
                subset=["username","platform"]
            )
            .reset_index(
                drop=True
            )
        )


        # Relevance score

        # Compute relevance scores (and extracted keywords) comparing each profile's text to the topic
        relevance, keywords = (
            RelevanceEngine
            .hybrid_relevance(
                df["text"],
                topic
            )
        )

        df["relevance_score"] = relevance
        # Remove unrelated influencers
        # Filter out influencers below the minimum relevance threshold
        df = df[
            df["relevance_score"] >= 0.30
        ].reset_index(drop=True)


        # Influence score

        # Calculate an influence score based on followers/engagement metrics
        df["influence_score"] = (
            RankingEngine
            .calculate_influence(
                df
            )
        )


        # Final score

        # Combine relevance + influence into a single overall ranking score
        df["overall_score"] = (
            RankingEngine
            .calculate_overall(
                df
            )
        )


        # Confidence

        # Calculate a confidence score for each influencer's result reliability
        df["confidence_score"] = (
            df.apply(
                ExplanationEngine.confidence_score,
                axis=1
            )
        )


        # Explanation

        # Generate a human-readable reason for why each influencer was selected
        df["selection_reason"] = (
            df.apply(
                lambda row:
                ExplanationEngine.selection_reason(
                    row,
                    topic
                ),
                axis=1
            )
        )


        # Ranking

        # Sort by overall score (highest first) and keep only the top N results
        df = (
            df
            .sort_values(
                "overall_score",
                ascending=False
            )
            .head(top_n)
            .reset_index(
                drop=True
            )
        )


        # Build the final list of result dictionaries to return
        results = []


        for idx, row in df.iterrows():

            results.append({

                "rank": idx + 1,  # Rank position (1-based)

                "username": row["username"],

                "category": row.get(
                    "category",
                    ""
                ),

                "platform": row.get(
                    "platform",
                    ""
                ),

                "followers": int(
                    row.get(
                        "followers",
                        0
                    )
                ),


                "relevance_score": round(
                    float(
                        row["relevance_score"]
                    ),
                    4
                ),


                "influence_score": round(
                    float(
                        row["influence_score"]
                    ),
                    4
                ),


                "overall_score": round(
                    float(
                        row["overall_score"]
                    ),
                    4
                ),


                "confidence_score": round(
                    float(
                        row["confidence_score"]
                    ),
                    1
                ),


                "selection_reason":
                    row["selection_reason"],

                # Top 5 keywords extracted during relevance scoring
                "keywords":
                    keywords[:5]

            })

        # Return the final ranked list of influencer results
        return results
