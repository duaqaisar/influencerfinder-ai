from scrapers.scraper_manager import ScraperManager
from services.scraper_ingestion_service import (
    ScraperIngestionService,
)
from services.embedding_cache import EmbeddingCache

# Orchestrates the full search pipeline: scrape -> ingest -> rebuild embeddings (if needed)
class SearchPipeline:

    @staticmethod
    def refresh(topic: str, limit: int = 20):
        print(f"[Pipeline] Scraping '{topic}'...")

        # Scrape influencers across all platforms for the given topic
        influencers = (
            ScraperManager()
            .search_all(
                query=topic,
                limit=limit,
            )
        )
        print(
            f"[Pipeline] Scraped {len(influencers)} influencers."
        )

        # Save the scraped influencer data into the database (insert/update)
        stats = (
            ScraperIngestionService
            .ingest(influencers)
        )
        print("[Pipeline] Database updated.")

        # Rebuild embeddings only if the database changed
        # Only rebuild embeddings if new data was actually inserted or updated (avoids unnecessary work)
        if (
            stats["inserted"] > 0
            or
            stats["updated"] > 0
        ):
            EmbeddingCache.refresh()
            print("[Pipeline] Embeddings rebuilt.")
        else:
            print(
                "[Pipeline] No database changes. Using existing embeddings."
            )
            # Ensure the existing cache is loaded
            # No new data, so just make sure the current cache is loaded and ready
            EmbeddingCache.ensure_ready()

        # Return ingestion stats (scraped/inserted/updated/skipped counts)
        return stats
