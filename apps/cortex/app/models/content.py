from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class WebhookRequest(BaseModel):
    url: HttpUrl

class Image(BaseModel):
    url: str
    alt: Optional[str] = None

class Content(BaseModel):
    url: str
    title: str
    markdown: str
    images: List[Image]
    metadata: dict
    created_at: datetime = datetime.utcnow() 