from sqlalchemy.orm import Session
from models.influencer import Influencer

# Repository layer handling all direct database operations for Influencer records
class InfluencerRepository:

    @staticmethod
    def get_all(db: Session):
        # Fetch all influencers from the database
        return db.query(Influencer).all()

    @staticmethod
    def get_by_username(db: Session, username: str):
        # Fetch a single influencer matching the exact username
        return (
            db.query(Influencer)
            .filter(Influencer.username == username)
            .first()
        )

    @staticmethod
    def get_by_platform(db: Session, platform: str):
        # Fetch all influencers matching a platform (case-insensitive match)
        return (
            db.query(Influencer)
            .filter(Influencer.platform.ilike(platform))
            .all()
        )

    @staticmethod
    def create(db: Session, influencer: Influencer):
        # Insert a new influencer record into the database
        db.add(influencer)
        db.commit()
        db.refresh(influencer)  # Refresh to get DB-generated fields (e.g. id, created_at)
        return influencer

    @staticmethod
    def update(db: Session, db_obj: Influencer, data: dict):
        # Update only the fields provided in `data` that exist on the model
        for key, value in data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def upsert(db: Session, data: dict):
        # Check if an influencer with this username already exists
        influencer = (
            db.query(Influencer)
            .filter(
                Influencer.username == data["username"]
            )
            .first()
        )
        if influencer:
            # If it exists, update the existing record
            return InfluencerRepository.update(
                db,
                influencer,
                data
            )
        # Otherwise, create a new influencer record
        influencer = Influencer(**data)
        return InfluencerRepository.create(
            db,
            influencer
        )

    @staticmethod
    def get_dataframe(db: Session, platform=None):
        # Fetch influencers, optionally filtered by platform
        if platform:
            influencers = (
                db.query(Influencer)
                .filter(
                    Influencer.platform.ilike(platform)
                )
                .all()
            )
        else:
            influencers = db.query(Influencer).all()

        # Convert influencer objects into a list of plain dictionaries (dataframe-friendly rows)
        rows = []
        for influencer in influencers:
            rows.append({
                "username": influencer.username,
                "followers": influencer.followers,
                "posts": influencer.posts_count,
                # Combined engagement metric (likes + comments)
                "eng_avg": influencer.avg_likes + influencer.avg_comments,
                # Combine category, bio, and full name into one searchable text field
                "text": " ".join(filter(None, [
                    influencer.category,
                    influencer.bio,
                    influencer.full_name
                ])),
                "platform": influencer.platform,
            })
        return rows
