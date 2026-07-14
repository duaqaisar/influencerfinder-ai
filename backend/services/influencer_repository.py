from sqlalchemy.orm import Session
from models.influencer import Influencer


class InfluencerRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Influencer).all()

    @staticmethod
    def get_by_username(db: Session, username: str):
        return (
            db.query(Influencer)
            .filter(Influencer.username == username)
            .first()
        )

    @staticmethod
    def get_by_platform(db: Session, platform: str):
        return (
            db.query(Influencer)
            .filter(Influencer.platform.ilike(platform))
            .all()
        )

    @staticmethod
    def create(db: Session, influencer: Influencer):
        db.add(influencer)
        db.commit()
        db.refresh(influencer)
        return influencer

    @staticmethod
    def update(db: Session, db_obj: Influencer, data: dict):

        for key, value in data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    @staticmethod
    def upsert(db: Session, data: dict):

        influencer = (
            db.query(Influencer)
            .filter(
                Influencer.username == data["username"]
            )
            .first()
        )

        if influencer:

            return InfluencerRepository.update(
                db,
                influencer,
                data
            )

        influencer = Influencer(**data)

        return InfluencerRepository.create(
            db,
            influencer
        )

    @staticmethod
    def get_dataframe(db: Session, platform=None):

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

        rows = []

        for influencer in influencers:

            rows.append({
                "username": influencer.username,
                "followers": influencer.followers,
                "posts": influencer.posts_count,
                "eng_avg": influencer.avg_likes + influencer.avg_comments,
                "text": " ".join(filter(None, [
                    influencer.category,
                    influencer.bio,
                    influencer.full_name
                ])),
                "platform": influencer.platform,
            })

        return rows
