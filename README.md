# Influencer Detective

An AI-powered tool that finds and ranks social media influencers by topic. You type in something like "fitness" or "music," and it scrapes creator data across Instagram, TikTok, YouTube, and Facebook, scores each profile for relevance and influence, and gives you a ranked shortlist with an explanation for why each one made the list.

Built as a bioinformatics student trying to apply ML/NLP concepts to a real, useful problem instead of another toy dataset.

## Why I built this

Finding the right influencer for a campaign usually means manually scrolling through four different apps, guessing at follower counts, and hoping the bio actually matches what you're looking for. I wanted to see if I could automate that  pull real data, embed it semantically, and rank by actual relevance instead of just follower count.

Turns out getting semantic search to behave (and not rank K-pop bands as "highly relevant to fitness") is harder than it sounds. More on that below.

## What it does

- Scrapes live creator data from Instagram, TikTok, YouTube, and Facebook via Apify
- Builds a profile for each creator and embeds it with a sentence-transformer model
- Scores relevance using a blend of keyword matching, TF-IDF, and semantic similarity
- Scores influence from followers, engagement rate, and posting activity
- Ranks results and generates a plain-language explanation for each one
- Shows a confidence score so you know how much data is actually behind a recommendation

## Stack

**Backend:** Python, FastAPI, SQLAlchemy + SQLite, Sentence Transformers, scikit-learn, pandas/numpy

**Frontend:** React + Vite, Framer Motion, Axios, plain CSS (no UI library , built the design system by hand)

**Scraping:** Apify actors for Instagram, TikTok, YouTube, Facebook

## How it's wired together

```
Search query (frontend)
        │
        ▼
FastAPI backend
        │
        ├─► Apify scrapers pull fresh data → SQLite
        │
        ├─► Sentence-transformer embeddings, cached
        │
        ▼
Relevance scoring (keyword + TF-IDF + semantic, blended)
        │
        ▼
Influence scoring (followers + engagement + activity)
        │
        ▼
Ranked results + confidence + explanation → frontend
```

## Running it locally

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You'll need your own API keys — create a `.env` in `backend/`:

```
APIFY_API_TOKEN=your_token
HF_TOKEN=your_token   # optional, avoids Hugging Face rate limits
```

Then:

```bash
uvicorn app.main:app --reload
```

Runs on `http://127.0.0.1:8000`, docs at `/docs`.

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`.

Heads up  Apify's free tier has a monthly compute cap, and I hit it more than once while building this. If scraping fails, the app still falls back to whatever's already in the SQLite database from a previous run.

## The hardest part

Getting the relevance scoring right. Early on, searching "fitness" returned NCT DREAM and Taylor Swift in the top results because raw semantic similarity between short bios and a topic word is noisy, and normalizing it stretched that noise into what looked like a confident signal. Had to gate semantic scoring behind actual keyword hits before it stopped ranking celebrities as fitness influencers. Also learned the hard way that mixing weighted scores across different scales (one maxing at 0.19, another at 1.0) quietly breaks your weights even if the numbers "look" balanced.

## About me

Dua Qaisar, bioinformatics undergrad
