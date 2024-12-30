from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from app.services.scraper import scrape_url
from app.models.content import Content

app = FastAPI(
    title="Cortex Content Scraper API",
    description="API for scraping web content and converting it to structured data",
    version="0.1.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="URL to scrape")
    added_by: Optional[str] = Field(default="api_user", description="User who added the content")

@app.post("/scrape", response_model=dict)
async def scrape_content(request: ScrapeRequest):
    """
    Scrape content from a given URL and return a structured Content object
    
    - **url**: The URL to scrape
    - **added_by**: Optional identifier for the user adding the content
    """
    try:
        # Scrape the URL 
        content = await scrape_url(request.url, request.added_by)
        
        # Convert Content object to a dictionary for JSON serialization
        content_dict = {
            "url": content.url,
            "domain": content.domain,
            "date_added": content.date_added.isoformat() if content.date_added else None,
            "date_published": content.date_published.isoformat() if content.date_published else None,
            "added_by": content.added_by,
            "authors": content.authors,
            "type": content.type.value,
            "tags": content.tags,
            "links": content.links,
            "markdown_content": content.markdown_content,
            "images": [
                {
                    "url": img.url,
                    "alt": img.alt,
                    "caption": img.caption
                } for img in content.images
            ],
            "metadata": content.metadata
        }
        
        return content_dict
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
