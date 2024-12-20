from pydantic import BaseModel, HttpUrl, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
from numpy.typing import NDArray

class ContentType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    PODCAST = "podcast"
    RESEARCH_PAPER = "research_paper"
    BLOG_POST = "blog_post"
    NEWS = "news"
    WEBSITE = "website"
    OTHER = "other"

class ContentLanguage(str, Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    OTHER = "other"

class WebhookRequest(BaseModel):
    url: HttpUrl
    added_by: str

class Image(BaseModel):
    url: str
    alt: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class Metadata(BaseModel):
    # Content Analysis
    word_count: Optional[int] = None
    reading_time_minutes: Optional[int] = None
    language: ContentLanguage = ContentLanguage.ENGLISH
    summary: Optional[str] = None
    key_takeaways: List[str] = Field(default_factory=list)
    
    # Academic/Research Specific
    doi: Optional[str] = None
    citations: Optional[List[str]] = Field(default_factory=list)
    journal: Optional[str] = None
    conference: Optional[str] = None
    
    # Media Information
    duration: Optional[timedelta] = None  # For videos/podcasts
    thumbnail_url: Optional[str] = None
    
    # Social/Engagement
    likes: Optional[int] = None
    shares: Optional[int] = None
    comments_count: Optional[int] = None
    
    # Source Information
    publisher: Optional[str] = None
    publication: Optional[str] = None
    paywall: Optional[bool] = None
    is_original: Optional[bool] = None
    
    # Classification
    topics: List[str] = Field(default_factory=list)  # Higher-level categories
    sentiment: Optional[float] = None  # -1 to 1 scale
    
    # Technical
    last_updated: Optional[datetime] = None
    word_frequency: Dict[str, int] = Field(default_factory=dict)
    
    # Custom fields for future expansion
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, *args, **kwargs) -> dict:
        """Convert to dictionary, excluding None values"""
        d = super().dict(*args, **kwargs)
        return {k: v for k, v in d.items() if v is not None}

class Content(BaseModel):
    id: Optional[UUID4] = None
    url: str
    domain: str
    date_added: datetime = Field(default_factory=datetime.utcnow)
    date_published: Optional[datetime] = None
    added_by: str
    authors: List[str] = Field(default_factory=list)
    type: ContentType = ContentType.ARTICLE
    tags: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)  # Just store URLs as strings
    markdown_content: str
    images: List[Image] = Field(default_factory=list)
    embedding: Optional[NDArray[np.float32]] = None
    metadata: Metadata = Field(default_factory=Metadata)

    class Config:
        arbitrary_types_allowed = True  # Required for numpy array support

    def get_text_for_embedding(self) -> str:
        """Get the text that should be used for generating embeddings"""
        parts = [
            self.metadata.summary or "",
            " ".join(self.metadata.key_takeaways),
            " ".join(self.tags),
            self.markdown_content
        ]
        return " ".join(part.strip() for part in parts if part.strip())

    def set_embedding(self, embedding: List[float]) -> None:
        """Set the embedding from a list of floats"""
        self.embedding = np.array(embedding, dtype=np.float32)

    def get_embedding_list(self) -> Optional[List[float]]:
        """Get the embedding as a list of floats for database storage"""
        if self.embedding is not None:
            return self.embedding.tolist()
        return None