from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Influencer:
    platform: str

    username: str
    display_name: str

    bio: str
    category: Optional[str] = None

    followers: int = 0
    following: int = 0

    posts: int = 0

    engagement_rate: float = 0.0

    verified: bool = False

    profile_url: str = ""
    profile_image: str = ""

    keywords: List[str] = field(default_factory=list)

    email: Optional[str] = None
    website: Optional[str] = None

    scraped_at: Optional[str] = None
