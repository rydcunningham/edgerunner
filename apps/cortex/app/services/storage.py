from supabase import create_client, Client
from app.config.settings import get_settings
from app.models.content import Content
from urllib.parse import urlparse
from typing import Optional

settings = get_settings()

def get_supabase_client() -> Optional[Client]:
    """Get Supabase client if credentials are available"""
    if settings.SUPABASE_URL and settings.SUPABASE_KEY and settings.SUPABASE_URL != "https://your-project.supabase.co":
        try:
            return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception as e:
            print(f"Warning: Failed to initialize Supabase client - {str(e)}")
    return None

def extract_domain(url: str) -> str:
    """Extract the domain from a URL"""
    parsed = urlparse(url)
    return parsed.netloc

async def store_content(content: Content) -> dict:
    """
    Stores the content in Supabase and returns the created record
    """
    # Get a fresh client instance each time
    supabase = get_supabase_client()
    
    if not supabase:
        print("Warning: Supabase not configured - skipping storage")
        return content.dict()
        
    try:
        # Convert Content model to dict for storage
        content_data = {
            "url": str(content.url),
            "domain": content.domain or extract_domain(str(content.url)),
            "date_added": content.date_added.isoformat(),
            "date_published": content.date_published.isoformat() if content.date_published else None,
            "added_by": content.added_by,
            "authors": content.authors,
            "type": content.type.value,
            "tags": content.tags,
            "links": content.links,  # Now just a list of strings
            "markdown_content": content.markdown_content,
            "images": [img.dict() for img in content.images],
            "metadata": content.metadata
        }
        
        # Insert into Supabase
        result = supabase.table("content").insert(content_data).execute()
        
        if not result.data:
            raise Exception("Failed to store content in Supabase")
            
        return result.data[0]
        
    except Exception as e:
        print(f"Warning: Error storing content in Supabase - {str(e)}")
        return content.dict() 