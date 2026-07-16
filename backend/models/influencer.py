from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

# ORM model representing an influencer in the database
class Influencer(Base):
    __tablename__ = "influencers"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each influencer
    username = Column(String, unique=True, index=True, nullable=False)  # Influencer's unique username (required)
    full_name = Column(String)              # Influencer's full/display name
    platform = Column(String)               # Platform they're on (e.g. Instagram, YouTube)
    bio = Column(Text)                      # Influencer's bio/description text
    category = Column(String)               # Content category/niche (e.g. fitness, tech)
    followers = Column(Integer, default=0)  # Total follower count
    following = Column(Integer, default=0)  # Total accounts they follow
    posts_count = Column(Integer, default=0)  # Total number of posts
    avg_likes = Column(Float, default=0)      # Average likes per post
    avg_comments = Column(Float, default=0)   # Average comments per post
    engagement_rate = Column(Float, default=0)  # Calculated engagement rate
    verified = Column(Boolean, default=False)   # Whether the account is verified
    profile_url = Column(String)              # Link to the influencer's profile
    relevance_score = Column(Float, default=0)  # Score indicating relevance to a search topic
    influence_score = Column(Float, default=0)  # Score indicating overall influence/reach
    overall_score = Column(Float, default=0)    # Combined final score (relevance + influence, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp when the record was created

    # One-to-many relationship: an influencer can have many posts
    posts = relationship(
        "Post",
        back_populates="influencer",       # Matching field on the Post model
        cascade="all, delete-orphan",      # Delete associated posts if the influencer is deleted
    )

    # String representation for debugging/logging (e.g. <Influencer johndoe>)
    def __repr__(self):
        return f"<Influencer {self.username}>"
