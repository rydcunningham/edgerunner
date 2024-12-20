from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.services.scraper import scrape_url
from app.models.content import WebhookRequest
from app.config.settings import get_settings
import markdown
from pathlib import Path

app = FastAPI(title="Cortex", description="URL content extraction and storage service")
settings = get_settings()

# Templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Add markdown filter to Jinja2 environment
templates.env.filters["markdown"] = lambda text: markdown.markdown(text or "", extensions=['tables', 'fenced_code'])

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process_url(request: Request, url: str = Form(...), added_by: str = Form(...)):
    try:
        content = await scrape_url(url, added_by)
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "content": content
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 