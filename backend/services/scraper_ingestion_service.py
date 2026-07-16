from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.influencer import Influencer

# Handles saving scraped influencer data into the database (insert new / update existing)
class ScraperIngestionService:

    @staticmethod
    def ingest(influencers):
        # Open a new database session
        db: Session = SessionLocal()

        # Counters to track ingestion results
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
                    # Refresh fields with the latest scraped data
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
                    # Guard against a username-only unique constraint conflict across platforms
                    username_exists = (
                        db.query(Influencer)
                        .filter(
                            Influencer.username == item.username
                        )
                        .first()
                    )
                    if username_exists:
                        # Skip insertion if the username is already taken by another record
                        skipped += 1
                        continue

                    # Create a new influencer record from the scraped item
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

            # Commit all inserts/updates in one transaction
            db.commit()
            # Return a summary of what happened during ingestion
            return {
                "scraped": len(influencers),
                "inserted": inserted,
                "updated": updated,
                "skipped": skipped,
            }
        except Exception as e:
            # Roll back all changes if anything goes wrong, then re-raise the error
            db.rollback()
            raise e
        finally:
            # Always close the session
            db.close()

    # Platform-specific wrapper methods that all reuse the shared ingest() logic
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
