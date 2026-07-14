from scrapers.scraper_manager import ScraperManager

from services.scraper_ingestion_service import (
    ScraperIngestionService,
)

from services.embedding_cache import EmbeddingCache


class SearchPipeline:

    @staticmethod
    def refresh(topic: str, limit: int = 20):

        print(f"[Pipeline] Scraping '{topic}'...")

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

        stats = (
            ScraperIngestionService
            .ingest(influencers)
        )

        print("[Pipeline] Database updated.")

        # Rebuild embeddings only if the database changed
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
            EmbeddingCache.ensure_ready()

        return stats
