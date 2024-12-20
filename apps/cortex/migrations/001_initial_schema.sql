-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Create enums for content types and languages
CREATE TYPE content_type AS ENUM (
    'article',
    'video',
    'podcast',
    'research_paper',
    'blog_post',
    'news',
    'other'
);

CREATE TYPE content_language AS ENUM (
    'en',
    'es',
    'fr',
    'de',
    'zh',
    'ja',
    'other'
);

-- Create the main content table
CREATE TABLE content (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    date_added TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    date_published TIMESTAMP WITH TIME ZONE,
    added_by TEXT NOT NULL,
    authors TEXT[] DEFAULT '{}',
    type content_type DEFAULT 'article' NOT NULL,
    tags TEXT[] DEFAULT '{}',
    links TEXT[] DEFAULT '{}',
    markdown_content TEXT NOT NULL,
    images JSONB DEFAULT '[]',
    embedding vector(1536),  -- OpenAI's text-embedding-ada-002 dimension
    metadata JSONB DEFAULT '{
        "word_count": null,
        "reading_time_minutes": null,
        "language": "en",
        "summary": null,
        "key_takeaways": [],
        "doi": null,
        "citations": [],
        "journal": null,
        "conference": null,
        "duration": null,
        "thumbnail_url": null,
        "likes": null,
        "shares": null,
        "comments_count": null,
        "publisher": null,
        "publication": null,
        "paywall": null,
        "is_original": null,
        "topics": [],
        "sentiment": null,
        "last_updated": null,
        "word_frequency": {},
        "custom_fields": {}
    }'::jsonb
);

-- Create indexes for common queries
CREATE INDEX idx_content_domain ON content(domain);
CREATE INDEX idx_content_date_added ON content(date_added);
CREATE INDEX idx_content_date_published ON content(date_published);
CREATE INDEX idx_content_added_by ON content(added_by);
CREATE INDEX idx_content_type ON content(type);

-- Create GIN indexes for array fields and full-text search
CREATE INDEX idx_content_markdown_content ON content USING gin(to_tsvector('english', markdown_content));
CREATE INDEX idx_content_authors ON content USING gin(authors);
CREATE INDEX idx_content_tags ON content USING gin(tags);
CREATE INDEX idx_content_links ON content USING gin(links);

-- Create GIN indexes for JSONB metadata fields we'll query often
CREATE INDEX idx_content_metadata ON content USING gin(metadata);
CREATE INDEX idx_content_metadata_publisher ON content USING gin((metadata -> 'publisher'));
CREATE INDEX idx_content_metadata_topics ON content USING gin((metadata -> 'topics'));
CREATE INDEX idx_content_metadata_language ON content USING btree((metadata ->> 'language'));

-- Create vector similarity search index
CREATE INDEX idx_content_embedding ON content USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- Number of lists can be tuned based on dataset size

-- Add helper functions
CREATE OR REPLACE FUNCTION extract_domain(url TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN split_part(split_part(url, '//', 2), '/', 1);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to calculate reading time
CREATE OR REPLACE FUNCTION calculate_reading_time(word_count INTEGER)
RETURNS INTEGER AS $$
BEGIN
    -- Average reading speed of 200-250 words per minute
    RETURN CEIL(word_count::float / 225);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to search content by topic
CREATE OR REPLACE FUNCTION search_by_topic(topic TEXT)
RETURNS TABLE (
    id UUID,
    url TEXT,
    title TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.url,
        c.metadata->>'title' as title,
        similarity(c.metadata->>'topics', topic) as similarity
    FROM content c
    WHERE 
        c.metadata->>'topics' % topic
    ORDER BY similarity DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to find similar content by embedding
CREATE OR REPLACE FUNCTION find_similar_content(query_embedding vector, match_threshold float, match_count int)
RETURNS TABLE (
    id UUID,
    url TEXT,
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.url,
        1 - (c.embedding <=> query_embedding) as similarity
    FROM content c
    WHERE c.embedding IS NOT NULL
    AND 1 - (c.embedding <=> query_embedding) > match_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql; 