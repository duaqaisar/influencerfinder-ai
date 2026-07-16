from core.database import SessionLocal
from models.influencer import Influencer

# Handles saving scraped YouTube channel data into the database (insert new / update existing)
class YouTubeIngestionService:

    @staticmethod
    def ingest(items):
        # Open a new database session
        db = SessionLocal()

        # Counters to track ingestion results
        inserted = 0
        updated = 0

        try:
            for item in items:
                # Determine the username, trying multiple possible fields as fallbacks,
                # and as a last resort extracting it from the channel URL
                username = (
                    item.get("channelName")
                    or item.get("channelTitle")
                    or item.get("channelUrl", "").split("@")[-1]
                )

                # Check if this YouTube channel already exists in the database
                existing = (
                    db.query(Influencer)
                    .filter_by(
                        username=username,
                        platform="YouTube"
                    )
                    .first()
                )
                if existing:
                    # If it exists, just update the follower/subscriber count
                    existing.followers = item.get(
                        "channelSubscribers",
                        existing.followers
                    )
                    updated += 1
                    continue

                # Otherwise, create a new Influencer record for this YouTube channel
                influencer = Influencer(
                    username=username,
                    full_name=item.get(
                        "channelName",
                        ""
                    ),
                    platform="YouTube",
                    bio="",
                    followers=item.get(
                        "channelSubscribers",
                        0
                    ),
                    posts_count=item.get(
                        "channelTotalVideos",
                        0
                    ),
                    verified=False,
                    profile_url=item.get(
                        "channelUrl",
                        ""
                    ),
                )
                db.add(influencer)
                inserted += 1

            # Commit all inserts/updates in one transaction
            db.commit()
            # Return a summary of what happened during ingestion
            return {
                "scraped": len(items),
                "inserted": inserted,
                "updated": updated
            }
        finally:
            # Always close the session, even if an error occurs
            db.close()
