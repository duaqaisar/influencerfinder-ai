from scrapers.platforms.instagram_scraper import InstagramScraper
from services.embedding_cache import EmbeddingCache
from services.influencer_profile_builder import InfluencerProfileBuilder
from services.scraper_ingestion_service import ScraperIngestionService

# Service that orchestrates scraping and ingesting influencer data
class ScraperService:

    @staticmethod
    def scrape_instagram(query: str, limit: int = 50):
        # Initialize the Instagram scraper
        scraper = InstagramScraper()
        # Search Instagram for influencers matching the query
        influencers = scraper.search(
            query=query,
            limit=limit,
        )
        # Save/ingest the scraped influencer data into the database
        result = ScraperIngestionService.ingest_instagram(
            influencers
        )
        # Rebuild influencer profiles (e.g. aggregated stats/summaries) after new data is ingested
        profiles = InfluencerProfileBuilder.build_profiles()
        # Rebuild the embedding cache using the updated profiles (for search/matching)
        EmbeddingCache.build(
            profiles
        )
        # Flag in the response indicating embeddings were refreshed
        result["embeddings_rebuilt"] = True
        return result
