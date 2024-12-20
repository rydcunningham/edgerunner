from supabase import create_client
from app.config.settings import get_settings
from app.models.content import Content

settings = get_settings()

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def store_content(content: Content) -> dict:
    """
    Stores the content in Supabase and returns the created record
    """
    try:
        # Convert Content model to dict for storage
        content_data = {
            "url": str(content.url),
            "title": content.title,
            "markdown": content.markdown,
            "images": [img.dict() for img in content.images],
            "metadata": content.metadata,
            "created_at": content.created_at.isoformat()
        }
        
        # Insert into Supabase
        result = supabase.table("content").insert(content_data).execute()
        
        if not result.data:
            raise Exception("Failed to store content in Supabase")
            
        return result.data[0]
        
    except Exception as e:
        raise Exception(f"Error storing content in Supabase: {str(e)}") 