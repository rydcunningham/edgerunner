import httpx
import trafilatura
from bs4 import BeautifulSoup
from datetime import datetime
import markdown
from urllib.parse import urlparse
from langdetect import detect
import pdfplumber
import magic
import io
import re
from app.config.settings import get_settings
from app.models.content import Content, Image, ContentType

settings = get_settings()

def parse_pdf_date(date_str: str) -> datetime | None:
    """
    Parse PDF date strings into datetime objects.
    Handles multiple formats:
    - D:20240410211143Z (PDF format used by arXiv)
    - 20240410211143 (Basic format)
    - 2024-04-10 (ISO format)
    """
    if not date_str:
        return None
        
    try:
        # Handle PDF format (D:YYYYMMDDHHmmSS[Z])
        if date_str.startswith('D:'):
            # Remove 'D:' prefix and 'Z' suffix if present
            date_str = date_str[2:].rstrip('Z')
            # Parse the basic format
            return datetime.strptime(date_str[:14], '%Y%m%d%H%M%S')
            
        # Try ISO format
        if '-' in date_str:
            return datetime.fromisoformat(date_str)
            
        # Try basic format
        if len(date_str) >= 8:  # At least YYYYMMDD
            return datetime.strptime(date_str[:8], '%Y%m%d')
            
    except (ValueError, TypeError):
        print(f"Could not parse date: {date_str}")
        return None
    
    return None

def clean_text(text: str) -> str:
    """Clean extracted text from PDF"""
    # Remove multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove hyphenation at end of lines
    text = re.sub(r'-\n', '', text)
    # Join lines that were split mid-sentence
    text = re.sub(r'([a-z])\n([a-z])', r'\1 \2', text, flags=re.IGNORECASE)
    return text.strip()

def pdf_to_markdown(pdf_content: bytes) -> tuple[str, dict]:
    """Convert PDF content to markdown and extract metadata"""
    metadata = {}
    text_blocks = []
    
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        # Extract metadata
        if pdf.metadata:
            metadata = {
                'title': pdf.metadata.get('Title', ''),
                'author': pdf.metadata.get('Author', ''),
                'date': parse_pdf_date(pdf.metadata.get('CreationDate')),
                'description': pdf.metadata.get('Subject', '')
            }
        
        # Process each page
        for i, page in enumerate(pdf.pages):
            if i == 0:  # First page special handling
                # Try to extract title from first page
                text = page.extract_text()
                if text and not metadata['title']:
                    # Usually the title is in the first few lines
                    first_lines = text.split('\n')[:3]
                    metadata['title'] = max(first_lines, key=len)
            
            text = page.extract_text()
            if text:
                text_blocks.append(clean_text(text))
    
    # Convert to markdown
    markdown_content = []
    
    # Add title
    if metadata.get('title'):
        markdown_content.append(f"# {metadata['title']}\n")
    
    # Add authors
    if metadata.get('author'):
        markdown_content.append(f"**Authors:** {metadata['author']}\n")
    
    # Add content
    markdown_content.extend(text_blocks)
    
    return '\n\n'.join(markdown_content), metadata

def is_substack_url(url: str) -> bool:
    """Check if the URL is from Substack"""
    return "substack.com" in urlparse(url).netloc

def is_paywalled(html: str) -> bool:
    """Check if the Substack article is paywalled"""
    soup = BeautifulSoup(html, 'lxml')
    
    # Common paywall indicators in Substack
    paywall_indicators = [
        "This post is for paid subscribers",
        "Subscribe to continue reading",
        "This is a preview of a paid post",
        "This post is for subscribers only",
        "Already a paid subscriber?"
    ]
    
    # Check for paywall text
    text = soup.get_text().lower()
    for indicator in paywall_indicators:
        if indicator.lower() in text:
            return True
            
    # Check for paywall-specific elements
    paywall_selectors = [
        ".paywall",
        ".paywall-banner",
        ".subscription-required",
        ".locked-post",
        "[data-component='PaywallBanner']"
    ]
    
    for selector in paywall_selectors:
        if soup.select(selector):
            return True
            
    return False

async def scrape_url(url: str, added_by: str) -> Content:
    """
    Scrapes the given URL using trafilatura and returns structured content
    """
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            print(f"Fetching URL: {url}")
            response = await client.get(url)
            response.raise_for_status()
            
            # Check if it's a Substack article
            is_substack = is_substack_url(url)
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            is_pdf = 'pdf' in content_type or url.lower().endswith('.pdf')
            
            if is_pdf:
                print("Detected PDF content, using PDF parser")
                content_bytes = response.content
                downloaded, pdf_metadata = pdf_to_markdown(content_bytes)
                metadata_dict = pdf_metadata
                
                # For PDFs, we don't extract images yet
                images = []
                links = []
                
            else:
                html = response.text
                print(f"Got HTML response of length: {len(html)}")
                
                # Check for paywall if it's a Substack article
                if is_substack and is_paywalled(html):
                    print("Detected paywalled Substack article")
                    # TODO: Add Substack2Markdown integration here
                    raise Exception("This is a paywalled Substack article. Subscription required.")

                # First try to get metadata
                metadata = trafilatura.extract_metadata(html)
                print(f"Extracted metadata: {metadata}")
                
                # Convert metadata to dict if it exists
                metadata_dict = {}
                if metadata:
                    metadata_dict = {
                        'title': metadata.title,
                        'author': metadata.author,
                        'date': metadata.date,
                        'sitename': metadata.sitename,
                        'description': metadata.description
                    }
                print(f"Processed metadata: {metadata_dict}")
                
                # Then extract main content in markdown format
                downloaded = trafilatura.extract(
                    html,
                    include_images=True,
                    include_links=True,
                    include_tables=True,
                    output_format='markdown',
                    with_metadata=True,
                    favor_precision=True,
                    include_comments=False,
                    no_fallback=False
                )

                if not downloaded:
                    print("Trafilatura extraction returned no content, trying with different settings...")
                    downloaded = trafilatura.extract(
                        html,
                        output_format='markdown',
                        include_images=True,
                        include_links=True,
                        favor_recall=True,
                        no_fallback=False
                    )
                    
                if not downloaded:
                    raise Exception("Failed to extract content with trafilatura after multiple attempts")
                
                print(f"Extracted content length: {len(downloaded)}")

                # Extract images using BeautifulSoup
                soup = BeautifulSoup(html, 'lxml')
                images = []
                base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
                
                # Find all images in the page
                for img in soup.find_all(['img', 'figure']):
                    # For figure elements, look for nested img
                    if img.name == 'figure':
                        img_tag = img.find('img')
                        if not img_tag:
                            continue
                        img = img_tag
                    
                    # Get all possible image sources
                    src = img.get('src', '')
                    if not src:
                        continue
                        
                    # Try to get the highest quality version of the image
                    img_url = (
                        img.get('data-src-large') or
                        img.get('data-large-file') or
                        img.get('data-src') or
                        img.get('data-original') or
                        img.get('data-full-src') or
                        src
                    ).strip()
                    
                    # Skip empty or data URLs
                    if not img_url or img_url.startswith('data:'):
                        continue
                        
                    # Handle various URL formats
                    if img_url.startswith('//'):
                        img_url = f"{urlparse(url).scheme}:{img_url}"
                    elif img_url.startswith('/'):
                        img_url = f"{base_url}{img_url}"
                    elif not img_url.startswith(('http://', 'https://')):
                        # Get the directory path of the current URL
                        url_parts = url.split('/')
                        if '.' in url_parts[-1]:  # If last part looks like a file
                            url_parts.pop()
                        base_path = '/'.join(url_parts)
                        img_url = f"{base_path.rstrip('/')}/{img_url.lstrip('/')}"
                    
                    # Clean up any double slashes (except after protocol)
                    img_url = img_url.replace('//', '//').replace('://', ':::').replace('//', '/').replace(':::', '://')
                    
                    # Get the best available caption
                    caption = None
                    if img.parent.name == 'figure':
                        figcaption = img.parent.find('figcaption')
                        if figcaption:
                            caption = figcaption.get_text(strip=True)
                    
                    if not caption:
                        caption = img.get('title') or img.get('alt') or ''
                    
                    print(f"Processing image URL: {img_url}")
                    
                    # Skip duplicates
                    if not any(existing.url == img_url for existing in images):
                        images.append(Image(
                            url=img_url,
                            alt=img.get('alt', ''),
                            caption=caption
                        ))
                
                print(f"Found {len(images)} images")

                # Extract links
                links = []
                for a in soup.find_all('a'):
                    href = a.get('href', '')
                    if href and href.startswith('http'):
                        links.append(href)
                print(f"Found {len(links)} links")

            # Determine content type (basic heuristic)
            content_type = ContentType.WEBSITE  # Default to website
            
            # Check for specific content types
            if is_pdf and ('arxiv.org' in url or 'doi.org' in url):
                content_type = ContentType.RESEARCH_PAPER
            elif '/video/' in url or 'youtube.com' in url or 'vimeo.com' in url:
                content_type = ContentType.VIDEO
            elif '/podcast/' in url or 'spotify.com/show' in url:
                content_type = ContentType.PODCAST
            elif 'arxiv.org' in url or 'doi.org' in url or '.edu' in urlparse(url).netloc:
                content_type = ContentType.RESEARCH_PAPER
            elif '/blog/' in url or 'medium.com' in url or metadata_dict.get('type') == 'blog':
                content_type = ContentType.BLOG_POST
            elif 'news' in url or any(domain in url for domain in ['reuters.com', 'bloomberg.com', 'nytimes.com']):
                content_type = ContentType.NEWS
            elif metadata_dict.get('type') == 'article' or '/article/' in url:
                content_type = ContentType.ARTICLE

            # Get authors from metadata if available
            authors = []
            if metadata_dict.get('author'):
                if isinstance(metadata_dict['author'], str):
                    # Split on common author separators
                    authors = [a.strip() for a in re.split(r'[,;]', metadata_dict['author'])]
                else:
                    authors = [metadata_dict['author']]

            # Create Content object
            content = Content(
                url=url,
                domain=urlparse(url).netloc,
                date_added=datetime.utcnow(),
                date_published=metadata_dict.get('date'),
                added_by=added_by,
                authors=authors,
                type=content_type,
                tags=[],  # Tags will be generated later
                links=links,
                markdown_content=downloaded or "",
                images=images,
                metadata={
                    "title": metadata_dict.get('title', ''),
                    "word_count": len(downloaded.split()) if downloaded else 0,
                    "reading_time_minutes": len(downloaded.split()) // 225 if downloaded else 0,  # Average reading speed
                    "is_original": True,  # Assuming direct source
                    "publisher": metadata_dict.get('sitename', ''),
                    "description": metadata_dict.get('description', ''),
                    "paywall": is_substack and is_paywalled(html) if not is_pdf else False
                }
            )

            return content
    except Exception as e:
        print(f"Error scraping URL: {str(e)}")
        raise Exception(f"Failed to extract content: {str(e)}") 