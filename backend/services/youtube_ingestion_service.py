from core.database import SessionLocal
from models.influencer import Influencer


class YouTubeIngestionService:

    @staticmethod
    def ingest(items):

        db = SessionLocal()

        inserted = 0
        updated = 0

        try:

            for item in items:

                username = (
                    item.get("channelName")
                    or item.get("channelTitle")
                    or item.get("channelUrl", "").split("@")[-1]
                )

                existing = (
                    db.query(Influencer)
                    .filter_by(
                        username=username,
                        platform="YouTube"
                    )
                    .first()
                )

                if existing:

                    existing.followers = item.get(
                        "channelSubscribers",
                        existing.followers
                    )

                    updated += 1

                    continue

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

            db.commit()

            return {
                "scraped": len(items),
                "inserted": inserted,
                "updated": updated
            }

        finally:

            db.close()
