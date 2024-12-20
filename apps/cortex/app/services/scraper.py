import httpx
from app.config.settings import get_settings
from app.models.content import Content, Image

settings = get_settings()

async def scrape_url(url: str) -> Content:
    """
    Scrapes the given URL using Firecrawl.dev API and returns structured content
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.firecrawl.dev/scrape",
            headers={
                "Authorization": f"Bearer {settings.FIRECRAWL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"url": url}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to scrape URL: {response.text}")
        
        data = response.json()
        
        # Process images from the response
        images = [
            Image(url=img["url"], alt=img.get("alt"))
            for img in data.get("images", [])
        ]
        
        # Create and return Content object
        return Content(
            url=url,
            title=data["title"],
            markdown=data["markdown"],
            images=images,
            metadata={
                "description": data.get("description"),
                "author": data.get("author"),
                "published_date": data.get("published_date"),
                "tags": data.get("tags", [])
            }
        ) 