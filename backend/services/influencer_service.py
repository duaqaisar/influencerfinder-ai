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



class InfluencerService:


    def find_influencers(
        self,
        topic: str,
        top_n: int = 10,
        platform: str = None
    ):

        SearchPipeline.refresh(
            topic=topic,
            limit=max(top_n, 20),
        )

        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        df = pd.DataFrame(
            profiles
        )



        # Platform filtering

        if platform:

            df = df[
                df["platform"]
                .astype(str)
                .str.lower()
                ==
                platform.lower()
            ]



        if df.empty:
            return {
                "message": "No influencers found."
            }



        # Cleaning

        df = df.fillna("")


        df = df[
            df["username"]
            .astype(str)
            .str.len()
            > 1
        ]



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

        relevance, keywords = (
            RelevanceEngine
            .hybrid_relevance(
                df["text"],
                topic
            )
        )

        df["relevance_score"] = relevance
        # Remove unrelated influencers
        df = df[
            df["relevance_score"] >= 0.30
        ].reset_index(drop=True)


        # Influence score

        df["influence_score"] = (
            RankingEngine
            .calculate_influence(
                df
            )
        )



        # Final score

        df["overall_score"] = (
            RankingEngine
            .calculate_overall(
                df
            )
        )



        # Confidence

        df["confidence_score"] = (
            df.apply(
                ExplanationEngine.confidence_score,
                axis=1
            )
        )



        # Explanation

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



        results = []



        for idx, row in df.iterrows():

            results.append({

                "rank": idx + 1,

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


                "keywords":
                    keywords[:5]

            })


        return results
