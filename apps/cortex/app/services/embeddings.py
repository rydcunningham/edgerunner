from typing import List
import openai
from app.config.settings import get_settings
from app.models.content import Content

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

async def create_embedding(text: str) -> List[float]:
    """Create an embedding using OpenAI's API"""
    response = await openai.Embedding.acreate(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

async def update_content_embedding(content: Content) -> Content:
    """Update the embedding for a piece of content"""
    # Get the text to embed
    text = content.get_text_for_embedding()
    
    # Create the embedding
    embedding = await create_embedding(text)
    
    # Set the embedding on the content
    content.set_embedding(embedding)
    
    return content

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings"""
    import numpy as np
    
    # Convert to numpy arrays
    a = np.array(embedding1)
    b = np.array(embedding2)
    
    # Calculate cosine similarity
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 