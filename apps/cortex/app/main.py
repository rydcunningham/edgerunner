from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.scraper import scrape_url
from app.services.storage import store_content
from app.models.content import WebhookRequest

app = FastAPI(title="Cortex", description="URL content extraction and storage service")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook")
async def process_webhook(request: WebhookRequest):
    try:
        # Extract content from URL using Firecrawl.dev
        content = await scrape_url(request.url)
        
        # Store the content in Supabase
        result = await store_content(content)
        
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 