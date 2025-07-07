import argparse
import redis
from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run
from microsearch.engine import SearchEngine  # Ensure this module exists

# Initialize FastAPI and Redis
app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
engine = SearchEngine()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_top_urls(scores_dict: dict, n: int):
    """Sorts search results by score and returns the top N results."""
    sorted_urls = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_urls[:n])

@app.get("/", response_class=HTMLResponse)
async def search(request: Request):
    """Renders the search page."""
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/results/{query}", response_class=HTMLResponse)
async def search_results(query: str = Path(...)):
    """Fetches search results dynamically from Redis and returns HTML for AJAX rendering."""
    results = engine.search(query)
    results = get_top_urls(results, n=5)
    
    results_html = "".join(
        [f"<div class='result-item'><a href='{url}'>🌐{url}</div>" for url, score in results.items()]
    )
    
    return results_html  # Sends raw HTML to be inserted dynamically

def load_data_from_redis():
    """Fetches all stored URLs and content from Redis and indexes them in the search engine."""
    all_data = redis_client.hgetall("web_crawl_data")
    content = list(all_data.items())  # Convert Redis hash to a list of (URL, content)
    engine.bulk_index(content)  # Index for search

if __name__ == "__main__":
    # Load data from Redis on startup
    load_data_from_redis()
    
    # Run FastAPI app
    run(app, host="192.168.0.123", port=8000)
