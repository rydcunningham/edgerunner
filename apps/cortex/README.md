# Cortex

A service that processes URLs from webhooks, extracts content using Firecrawl.dev, and stores structured data in Supabase.

## Features

- Webhook endpoint for URL processing
- Content extraction using Firecrawl.dev API
- Markdown and image extraction
- Structured data storage in Supabase
- Async processing

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
FIRECRAWL_API_KEY=your_firecrawl_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### POST /webhook
Accepts a URL and processes it through Firecrawl.dev, storing the results in Supabase.

Request body:
```json
{
    "url": "https://example.com/article"
}
```

### GET /health
Health check endpoint.

## Database Schema

The Supabase database should have a `content` table with the following structure:

```sql
create table content (
    id uuid default uuid_generate_v4() primary key,
    url text not null,
    title text not null,
    markdown text not null,
    images jsonb,
    metadata jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now())
);
```
