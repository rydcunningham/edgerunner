from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, String, DateTime, JSON, Text, Integer, Float, ForeignKey, Table
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.sql import text
from datetime import datetime
from typing import List, Optional
import numpy as np
from pathlib import Path

# Create database directory if it doesn't exist
db_dir = Path(__file__).parent.parent / "data"
db_dir.mkdir(exist_ok=True)
db_path = db_dir / "cortex.db"

# Create async engine
engine = create_async_engine(
    f"sqlite+aiosqlite:///{db_path}",
    echo=True  # Set to False in production
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

class Content(Base):
    __tablename__ = "content"
    
    id = Column(String, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    domain = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_published = Column(DateTime, nullable=True)
    added_by = Column(String, nullable=False)
    authors = Column(SQLiteJSON, default=list)
    type = Column(String, nullable=False)
    tags = Column(SQLiteJSON, default=list)
    links = Column(SQLiteJSON, default=list)
    markdown_content = Column(Text, nullable=False)
    images = Column(SQLiteJSON, default=list)
    content_metadata = Column(SQLiteJSON, default=dict)
    embedding = Column(SQLiteJSON, nullable=True)  # Store as JSON array

async def init_db():
    """Initialize the database with vector search capabilities"""
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Enable vector similarity search extension
        try:
            await conn.execute(text("CREATE VIRTUAL TABLE IF NOT EXISTS vss_content USING vss0(embedding(1536));"))
        except Exception as e:
            print(f"Warning: Could not create VSS table - {str(e)}")

async def get_session() -> AsyncSession:
    """Get a database session"""
    async with async_session() as session:
        yield session

async def store_content(content_model) -> dict:
    """Store content in the database"""
    async with async_session() as session:
        # Convert Pydantic model to SQLAlchemy model
        content = Content(
            id=content_model.id,
            url=content_model.url,
            domain=content_model.domain,
            date_added=content_model.date_added,
            date_published=content_model.date_published,
            added_by=content_model.added_by,
            authors=content_model.authors,
            type=content_model.type.value,
            tags=content_model.tags,
            links=content_model.links,
            markdown_content=content_model.markdown_content,
            images=[img.dict() for img in content_model.images],
            content_metadata=content_model.metadata.dict(),
            embedding=content_model.get_embedding_list()
        )
        
        session.add(content)
        await session.commit()
        await session.refresh(content)
        
        # Convert SQLAlchemy model back to dict
        return {
            "id": content.id,
            "url": content.url,
            "domain": content.domain,
            "date_added": content.date_added,
            "date_published": content.date_published,
            "added_by": content.added_by,
            "authors": content.authors,
            "type": content.type,
            "tags": content.tags,
            "links": content.links,
            "markdown_content": content.markdown_content,
            "images": content.images,
            "metadata": content.content_metadata,
            "embedding": content.embedding
        }

async def find_similar_content(embedding: List[float], threshold: float = 0.8, limit: int = 5) -> List[dict]:
    """Find similar content using vector similarity search"""
    async with async_session() as session:
        embedding_str = ','.join(map(str, embedding))
        query = text(f"""
            SELECT c.*, vss_content.distance
            FROM content c
            JOIN vss_content ON c.id = vss_content.rowid
            WHERE vss_content.distance > :threshold
            ORDER BY vss_content.distance DESC
            LIMIT :limit
        """)
        
        result = await session.execute(
            query,
            {"embedding": f"[{embedding_str}]", "threshold": threshold, "limit": limit}
        )
        
        return result.mappings().all() 

async def get_all_content() -> List[dict]:
    """Fetch all content from the database"""
    async with async_session() as session:
        result = await session.execute(
            text("SELECT * FROM content ORDER BY date_added DESC")
        )
        return [dict(row) for row in result.mappings()]