import pandas as pd

from core.database import SessionLocal
from models.influencer import Influencer


class InfluencerProfileBuilder:


    @staticmethod
    def clean_text(value):

        if value is None:
            return ""

        return str(value).strip()



    @classmethod
    def build_profiles(cls):

        db = SessionLocal()

        try:

            influencers = (
                db.query(Influencer)
                .order_by(Influencer.id)
                .all()
            )


            profiles = []


            for influencer in influencers:


                username = cls.clean_text(
                    influencer.username
                )

                full_name = cls.clean_text(
                    influencer.full_name
                )

                platform = cls.clean_text(
                    influencer.platform
                )

                category = cls.clean_text(
                    influencer.category
                )

                bio = cls.clean_text(
                    influencer.bio
                )


                #
                # IMPORTANT:
                # This text is used by the embedding model.
                # More information = better relevance scores.
                #
                text_parts = [

                    username,

                    full_name,

                    platform,

                    category,

                    bio

                ]


                text = " ".join(
                    [
                        part
                        for part in text_parts
                        if part
                    ]
                )


                profile = {

                    "id":
                        influencer.id,


                    "username":
                        username,


                    "full_name":
                        full_name,


                    "platform":
                        platform,


                    "category":
                        category,


                    "bio":
                        bio,


                    "followers":
                        influencer.followers or 0,


                    "following":
                        influencer.following or 0,


                    "posts_count":
                        influencer.posts_count or 0,


                    "avg_likes":
                        influencer.avg_likes or 0,


                    "avg_comments":
                        influencer.avg_comments or 0,


                    "engagement_rate":
                        influencer.engagement_rate or 0,


                    "verified":
                        influencer.verified or 0,


                    "text":
                        text

                }


                profiles.append(
                    profile
                )


            print(
                f"[ProfileBuilder] Built {len(profiles)} profiles"
            )


            return profiles


        finally:

            db.close()
