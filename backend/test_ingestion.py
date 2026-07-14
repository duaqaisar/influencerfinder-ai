from core.database import SessionLocal

from services.scraper_ingestion_service import (
    ScraperIngestionService,
)

db = SessionLocal()

service = ScraperIngestionService()

result = service.ingest_instagram(
    db=db,
    query="fitness",
    limit=5
)

print(result)

db.close()
