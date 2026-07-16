from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.config import get_settings
from services.influencer_service import InfluencerService
from scrapers.scraper_service import ScraperService

# Load application settings (env vars, app name, version, debug flag, etc.)
settings = get_settings()

# Initialize the FastAPI app instance with metadata from settings
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Enable CORS so the API can be called from any origin (useful for frontend apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow requests from all domains
    allow_credentials=True,    # Allow cookies/auth headers to be sent
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],       # Allow all headers in requests
)

# -----------------------------
# Request Models
# -----------------------------

# Schema for the Instagram scrape request body
class InstagramScrapeRequest(BaseModel):
    query: str          # Search term/keyword to scrape Instagram for
    limit: int = 20      # Max number of results to scrape (default 20)

# -----------------------------
# Root Endpoint
# -----------------------------

# Simple health-check / welcome endpoint
@app.get("/")
async def root():
    return {
        "message": "Influencer Finder API is running",
        "docs": "/docs"
    }

# -----------------------------
# AI Influencer Search
# -----------------------------

# Endpoint to search/find influencers based on a given topic
@app.get("/influencers")
async def get_influencers(
    topic: str = Query(..., description="Topic to search for"),   # Required search topic
    top_n: int = Query(
        10,
        description="Number of top influencers"
    ),  # How many top influencers to return (default 10)
    platform: str = Query(
        None,
        description="Filter by platform"
    )  # Optional platform filter (e.g. Instagram, YouTube)
):
    # Instantiate the influencer service
    service = InfluencerService()
    # Call the service to fetch matching influencers
    results = service.find_influencers(
        topic=topic,
        top_n=top_n,
        platform=platform
    )
    return results

# -----------------------------
# Instagram Scraper
# -----------------------------

# Endpoint to trigger an Instagram scrape based on a query and limit
@app.post("/scrape/instagram")
async def scrape_instagram(
    request: InstagramScrapeRequest
):
    # Call the scraper service to perform the actual scraping
    result = ScraperService.scrape_instagram(
        query=request.query,
        limit=request.limit
    )
    return result

# Entry point for running the app directly (e.g. `python main.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",   # Path to the FastAPI app instance
        host="0.0.0.0",   # Listen on all network interfaces
        port=8000,        # Port to run the server on
        reload=True,      # Auto-reload on code changes (dev mode)
    )
