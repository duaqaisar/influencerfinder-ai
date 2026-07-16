import pandas as pd
from core.database import SessionLocal
from models.influencer import Influencer

# Builds combined text profiles for each influencer using ORM queries (used later for embeddings/search)
class InfluencerProfileBuilder:

    @staticmethod
    def clean_text(value):
        # Replace None with an empty string, otherwise convert to string and strip whitespace
        if value is None:
            return ""
        return str(value).strip()

    @classmethod
    def build_profiles(cls):
        # Open a new database session
        db = SessionLocal()
        try:
            # Fetch all influencers from the database, ordered by ID
            influencers = (
                db.query(Influencer)
                .order_by(Influencer.id)
                .all()
            )

            profiles = []
            for influencer in influencers:
                # Clean each text field for this influencer
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
                # Combine all relevant text fields into a list
                text_parts = [
                    username,
                    full_name,
                    platform,
                    category,
                    bio
                ]
                # Join only the non-empty parts into a single text blob
                text = " ".join(
                    [
                        part
                        for part in text_parts
                        if part
                    ]
                )

                # Build the final profile dictionary with cleaned + numeric fields
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

            # Log how many profiles were successfully built
            print(
                f"[ProfileBuilder] Built {len(profiles)} profiles"
            )
            return profiles
        finally:
            # Always close the database session, even if an error occurs
            db.close()
