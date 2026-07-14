from scrapers.platforms.instagram_scraper import InstagramScraper

from services.embedding_cache import EmbeddingCache
from services.influencer_profile_builder import InfluencerProfileBuilder

from services.scraper_ingestion_service import ScraperIngestionService

class ScraperService:

    @staticmethod
    def scrape_instagram(query: str, limit: int = 50):

        scraper = InstagramScraper()

        influencers = scraper.search(
            query=query,
            limit=limit,
        )

        result = ScraperIngestionService.ingest_instagram(
            influencers
        )

        profiles = InfluencerProfileBuilder.build_profiles()

        EmbeddingCache.build(
            profiles
        )

        result["embeddings_rebuilt"] = True

        return result
