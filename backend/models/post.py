from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

# ORM model representing a single post made by an influencer
class Post(Base):
    __tablename__ = "posts"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each post
    influencer_id = Column(
        Integer,
        ForeignKey("influencers.id"),  # Links this post to its owning influencer
        nullable=False,                 # Every post must belong to an influencer
    )
    platform = Column(String, index=True)   # Platform the post was made on (e.g. Instagram)
    caption = Column(Text)                  # Post caption/text content
    hashtags = Column(JSON)                 # List of hashtags used, stored as JSON
    likes = Column(Integer, default=0)      # Number of likes on the post
    comments = Column(Integer, default=0)   # Number of comments on the post
    shares = Column(Integer, default=0)     # Number of shares/reposts
    views = Column(Integer, default=0)      # Number of views (relevant for video/reel posts)
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the post was made/recorded
    post_url = Column(String, nullable=True)  # Direct link to the post (optional)

    # Many-to-one relationship: each post belongs to one influencer
    influencer = relationship(
        "Influencer",
        back_populates="posts",  # Matching field on the Influencer model
    )

    # String representation for debugging/logging (e.g. <Post 42>)
    def __repr__(self):
        return f"<Post {self.id}>"
