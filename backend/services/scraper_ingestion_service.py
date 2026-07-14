from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.influencer import Influencer


class ScraperIngestionService:

    @staticmethod
    def ingest(influencers):

        db: Session = SessionLocal()

        inserted = 0
        updated = 0
        skipped = 0

        try:

            for item in influencers:

                # Check existing influencer by username + platform
                existing = (
                    db.query(Influencer)
                    .filter(
                        Influencer.username == item.username,
                        Influencer.platform == item.platform,
                    )
                    .first()
                )

                if existing:

                    # Update existing influencer
                    existing.full_name = item.display_name
                    existing.bio = item.bio
                    existing.category = item.category
                    existing.followers = item.followers
                    existing.following = item.following
                    existing.posts_count = item.posts
                    existing.profile_url = item.profile_url
                    existing.verified = item.verified

                    updated += 1

                else:

                    # Before inserting, check username collision
                    # because old schema may have username UNIQUE
                    username_exists = (
                        db.query(Influencer)
                        .filter(
                            Influencer.username == item.username
                        )
                        .first()
                    )

                    if username_exists:

                        skipped += 1
                        continue


                    influencer = Influencer(
                        username=item.username,
                        full_name=item.display_name,
                        platform=item.platform,
                        category=item.category,
                        bio=item.bio,
                        followers=item.followers,
                        following=item.following,
                        posts_count=item.posts,
                        verified=item.verified,
                        profile_url=item.profile_url,
                    )

                    db.add(influencer)

                    inserted += 1


            db.commit()


            return {
                "scraped": len(influencers),
                "inserted": inserted,
                "updated": updated,
                "skipped": skipped,
            }


        except Exception as e:

            db.rollback()
            raise e


        finally:

            db.close()



    @staticmethod
    def ingest_instagram(influencers):
        return ScraperIngestionService.ingest(influencers)


    @staticmethod
    def ingest_tiktok(influencers):
        return ScraperIngestionService.ingest(influencers)


    @staticmethod
    def ingest_youtube(influencers):
        return ScraperIngestionService.ingest(influencers)


    @staticmethod
    def ingest_facebook(influencers):
        return ScraperIngestionService.ingest(influencers)
