# Cortex Content Scraper API

## Overview
Cortex is a powerful web content scraping API that converts web URLs into structured, machine-readable content.

## Features
- Scrape web pages, PDFs, and various content types
- Extract metadata, markdown content, images, and links
- Support for multiple content types (research papers, blogs, news, etc.)

## Prerequisites
- Python 3.9+
- pip

## Installation
1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the API and Web App

### Options
```bash
# Run web app only (default port 11168)
python main.py app

# Run API only (default port 11169)
python main.py api

# Run both web app and API simultaneously
python main.py both

# Specify custom ports
python main.py app --app-port 8080
python main.py api --api-port 8081
python main.py both --app-port 8080 --api-port 8081
```

### Web App
- Accessible at `http://localhost:11168`
- Provides a user-friendly interface for URL scraping

### API
- Accessible at `http://localhost:11169`
- JSON endpoint for programmatic URL scraping
- Swagger UI available at `/docs`

## API Endpoint
### POST `/scrape`
Scrape content from a given URL

#### Request Body
```json
{
    "url": "https://example.com/article",
    "added_by": "optional_user_identifier"
}
```

#### Response
A JSON object containing:
- `url`: Original URL
- `domain`: Website domain
- `date_added`: Timestamp of scraping
- `date_published`: Original publication date
- `authors`: List of authors
- `type`: Content type (WEBSITE, RESEARCH_PAPER, etc.)
- `markdown_content`: Extracted text in markdown
- `images`: List of images with URLs and captions
- `metadata`: Additional content metadata

## Error Handling
- 400 Bad Request: Invalid URL or scraping failure
- Detailed error messages in response body

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.
