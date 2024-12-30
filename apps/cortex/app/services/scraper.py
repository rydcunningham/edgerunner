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
import arxiv
import markitdown
from app.config.settings import get_settings
from app.models.content import Content, Image, ContentType, Metadata

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
    """
    Convert PDF content to markdown using MarkItDown
    
    Returns:
    - Markdown content
    - Metadata dictionary
    """
    try:
        # Use MarkItDown to convert PDF to markdown
        from markitdown import MarkItDown
        
        # Initialize MarkItDown
        md = MarkItDown()
        
        # Create a temporary file for the PDF
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name
        
        try:
            # Convert PDF to markdown
            result = md.convert(temp_file_path)
            markdown_content = result.text_content
        finally:
            # Clean up the temporary file
            import os
            os.unlink(temp_file_path)
        
        # Try to extract metadata using pdfplumber as a fallback
        metadata = {}
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                if pdf.metadata:
                    metadata = {
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'date': parse_pdf_date(pdf.metadata.get('CreationDate')),
                        'description': pdf.metadata.get('Subject', '')
                    }
        except Exception as e:
            print(f"Metadata extraction failed: {e}")
        
        # Clean up the markdown content
        cleaned_content = clean_text(markdown_content)
        
        return cleaned_content, metadata
    
    except Exception as e:
        print(f"PDF to markdown conversion failed: {e}")
        
        # Fallback to pdfplumber if MarkItDown fails
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                # Extract text from all pages
                text_blocks = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_blocks.append(clean_text(text))
                
                # Combine text blocks
                markdown_content = '\n\n'.join(text_blocks)
                
                # Extract metadata
                metadata = {}
                if pdf.metadata:
                    metadata = {
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'date': parse_pdf_date(pdf.metadata.get('CreationDate')),
                        'description': pdf.metadata.get('Subject', '')
                    }
                
                return markdown_content, metadata
        
        except Exception as fallback_error:
            print(f"Fallback PDF extraction failed: {fallback_error}")
            return "", {}

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

class ContentScraper:
    @staticmethod
    def is_arxiv_url(url: str) -> bool:
        """Check if the URL is from arXiv"""
        return 'arxiv.org' in urlparse(url).netloc

    @staticmethod
    def is_substack_url(url: str) -> bool:
        """Check if the URL is from Substack"""
        return "substack.com" in urlparse(url).netloc

    @classmethod
    async def _extract_arxiv_content(cls, url: str, paper: arxiv.Result) -> dict:
        """
        Extract full content from arXiv paper, trying HTML first, then PDF
        
        Returns a dictionary with:
        - markdown_content: Extracted text
        - images: List of images found
        - links: List of links found
        """
        # Try HTML version first
        html_url = url.replace('/abs/', '/html/')
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(html_url)
                if response.status_code == 200:
                    # Extract markdown from HTML
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'lxml')
                    
                    # Find the main content div
                    content_div = soup.find('div', class_='ltx_page_content')
                    if content_div:
                        # Convert to markdown
                        markdown_content = cls._html_to_markdown(content_div)
                        
                        # Extract images
                        images = []
                        for img in soup.find_all('img'):
                            img_url = img.get('src', '')
                            if img_url and not img_url.startswith('data:'):
                                # Resolve relative URLs
                                if img_url.startswith('//'):
                                    img_url = f"https:{img_url}"
                                elif img_url.startswith('/'):
                                    img_url = f"https://arxiv.org{img_url}"
                                
                                images.append(Image(
                                    url=img_url,
                                    alt=img.get('alt', ''),
                                    caption=img.get('title', '')
                                ))
                        
                        # Extract links
                        links = []
                        current_paper_id = url.split('/')[-1].split('v')[0]
                        for a in soup.find_all('a', href=True):
                            href = a['href']
                            # Filter out self-referential arXiv links and citations
                            if href.startswith('http'):
                                # Skip links containing the current paper's ID
                                if current_paper_id not in href:
                                    links.append(href)
                            elif href.startswith('/'):
                                full_url = f"https://arxiv.org{href}"
                                # Skip links containing the current paper's ID
                                if current_paper_id not in full_url:
                                    links.append(full_url)
                        
                        # Remove duplicate links while preserving order
                        unique_links = []
                        seen_links = set()
                        for link in links:
                            if link not in seen_links:
                                unique_links.append(link)
                                seen_links.add(link)
                        
                        return {
                            'markdown_content': markdown_content,
                            'images': images,
                            'links': unique_links
                        }
        except Exception as e:
            print(f"HTML extraction failed for {url}: {e}")
        
        # Fallback to PDF
        try:
            # Download PDF
            async with httpx.AsyncClient() as client:
                pdf_response = await client.get(paper.pdf_url)
                if pdf_response.status_code == 200:
                    # Convert PDF to markdown
                    downloaded, _ = pdf_to_markdown(pdf_response.content)
                    return {
                        'markdown_content': downloaded,
                        'images': [],
                        'links': [paper.pdf_url]
                    }
        except Exception as e:
            print(f"PDF extraction failed for {url}: {e}")
        
        # If all else fails, return the abstract
        return {
            'markdown_content': paper.summary,
            'images': [],
            'links': [paper.pdf_url]
        }

    @staticmethod
    def _html_to_markdown(soup_element):
        """Convert HTML to markdown"""
        # Basic conversion, can be expanded
        markdown_content = []
        
        # Convert paragraphs
        for p in soup_element.find_all('p'):
            markdown_content.append(p.get_text())
        
        # Convert headings
        for h in soup_element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(h.name[1])
            markdown_content.append(f"{'#' * level} {h.get_text()}")
        
        return '\n\n'.join(markdown_content)

    @classmethod
    async def scrape_arxiv(cls, url: str, added_by: str) -> Content:
        """
        Specialized scraping method for arXiv papers
        """
        try:
            # Extract arXiv ID from URL
            arxiv_id = url.split('/')[-1].split('v')[0]
            
            # Search for the paper using arXiv API
            client = arxiv.Client()
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(client.results(search), None)
            
            if not paper:
                raise ValueError(f"No paper found for arXiv ID: {arxiv_id}")
            
            # Extract full content
            content_dict = await cls._extract_arxiv_content(url, paper)
            markdown_content = content_dict['markdown_content']
            
            # Calculate word count and reading time
            word_count = len(markdown_content.split())
            reading_time_minutes = max(1, word_count // 225)  # Average reading speed
            
            # Prepare metadata
            metadata = Metadata(
                word_count=word_count,
                reading_time_minutes=reading_time_minutes,
                doi=paper.doi,
                citations=[],  # TODO: Implement citation extraction
                journal=None,  # arXiv is a preprint server
                summary=paper.summary,
                last_updated=paper.updated,
                publisher="arXiv",
                topics=list(paper.categories),
                custom_fields={
                    "primary_category": paper.primary_category
                }
            )
            
            # Convert arXiv metadata to our Content model
            return Content(
                url=url,
                domain='arxiv.org',
                date_added=datetime.utcnow(),
                date_published=paper.published.date(),
                added_by=added_by,
                authors=[author.name for author in paper.authors],
                type=ContentType.RESEARCH_PAPER,
                tags=list(paper.categories),
                links=content_dict['links'],
                markdown_content=markdown_content,
                images=content_dict['images'],
                metadata=metadata
            )
        
        except Exception as arxiv_error:
            print(f"arXiv API failed for {url}: {arxiv_error}")
            raise

    @classmethod
    async def scrape_substack(cls, url: str, added_by: str, html: str) -> Content:
        """
        Specialized scraping method for Substack articles
        """
        # Check for paywall
        if is_paywalled(html):
            raise Exception("This is a paywalled Substack article. Subscription required.")
        
        # Use existing trafilatura extraction logic
        metadata = trafilatura.extract_metadata(html)
        
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
        
        # Extract main content
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
            downloaded = trafilatura.extract(
                html,
                output_format='markdown',
                include_images=True,
                include_links=True,
                favor_recall=True,
                no_fallback=False
            )
        
        if not downloaded:
            raise Exception("Failed to extract content with trafilatura")
        
        # Extract images and links (reuse existing logic from original scrape_url)
        soup = BeautifulSoup(html, 'lxml')
        images = []
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        
        # Find all images in the page (reuse existing image extraction logic)
        for img in soup.find_all(['img', 'figure']):
            # Existing image extraction logic here...
            pass
        
        return Content(
            url=url,
            domain=urlparse(url).netloc,
            date_added=datetime.utcnow(),
            date_published=metadata_dict.get('date'),
            added_by=added_by,
            authors=[metadata_dict.get('author')] if metadata_dict.get('author') else [],
            type=ContentType.BLOG_POST,
            tags=[],
            links=[],  # Populate with extracted links
            markdown_content=downloaded,
            images=images,
            metadata=metadata_dict
        )

    @classmethod
    async def scrape_url(cls, url: str, added_by: str) -> Content:
        """
        Main scraping method with triage logic
        """
        try:
            # Remove query parameters
            clean_url = url.split('?')[0]
            
            # Specialized scraping for arXiv
            if cls.is_arxiv_url(clean_url):
                return await cls.scrape_arxiv(clean_url, added_by)
            
            # Specialized scraping for Substack
            if cls.is_substack_url(clean_url):
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    response = await client.get(clean_url)
                    return await cls.scrape_substack(clean_url, added_by, response.text)
            
            # Default scraping logic
            async with httpx.AsyncClient(follow_redirects=True) as client:
                print(f"Fetching URL: {clean_url}")
                response = await client.get(clean_url)
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get('content-type', '').lower()
                is_pdf = 'pdf' in content_type or clean_url.lower().endswith('.pdf')
                
                # PDF handling
                if is_pdf:
                    content_bytes = response.content
                    downloaded, pdf_metadata = pdf_to_markdown(content_bytes)
                    
                    # Calculate word count and reading time
                    word_count = len(downloaded.split())
                    reading_time_minutes = max(1, word_count // 225)
                    
                    # Prepare metadata
                    metadata = Metadata(
                        word_count=word_count,
                        reading_time_minutes=reading_time_minutes,
                        publisher=urlparse(clean_url).netloc
                    )
                    
                    return Content(
                        url=clean_url,
                        domain=urlparse(clean_url).netloc,
                        date_added=datetime.utcnow(),
                        added_by=added_by,
                        type=ContentType.ARTICLE,
                        markdown_content=downloaded,
                        metadata=metadata
                    )
                
                # HTML handling
                html = response.text
                
                # Use trafilatura for content extraction
                metadata_obj = trafilatura.extract_metadata(html)
                
                # Extract main content
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
                
                # Fallback if extraction fails
                if not downloaded:
                    downloaded = trafilatura.extract(
                        html,
                        output_format='markdown',
                        include_images=True,
                        include_links=True,
                        favor_recall=True,
                        no_fallback=False
                    )
                
                # If still no content, use a basic extraction
                if not downloaded:
                    soup = BeautifulSoup(html, 'lxml')
                    downloaded = soup.get_text()
                
                # Extract images
                soup = BeautifulSoup(html, 'lxml')
                images = []
                for img in soup.find_all(['img', 'figure']):
                    # For figure elements, look for nested img
                    if img.name == 'figure':
                        img_tag = img.find('img')
                        if not img_tag:
                            continue
                        img = img_tag
                    
                    # Get image URL
                    img_url = img.get('src', '')
                    if not img_url or img_url.startswith('data:'):
                        continue
                    
                    # Resolve relative URLs
                    if img_url.startswith('//'):
                        img_url = f"{urlparse(clean_url).scheme}:{img_url}"
                    elif img_url.startswith('/'):
                        img_url = f"{urlparse(clean_url).scheme}://{urlparse(clean_url).netloc}{img_url}"
                    
                    images.append(Image(
                        url=img_url,
                        alt=img.get('alt', ''),
                        caption=img.get('title', '')
                    ))
                
                # Extract links
                links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('http'):
                        links.append(href)
                    elif href.startswith('/'):
                        links.append(f"{urlparse(clean_url).scheme}://{urlparse(clean_url).netloc}{href}")
                
                # Remove duplicate links while preserving order
                unique_links = []
                seen_links = set()
                for link in links:
                    if link not in seen_links:
                        unique_links.append(link)
                        seen_links.add(link)
                
                # Calculate word count and reading time
                word_count = len(downloaded.split())
                reading_time_minutes = max(1, word_count // 225)
                
                # Prepare metadata
                metadata = Metadata(
                    word_count=word_count,
                    reading_time_minutes=reading_time_minutes,
                    publisher=urlparse(clean_url).netloc,
                    title=metadata_obj.title if metadata_obj else None,
                    description=metadata_obj.description if metadata_obj else None,
                    last_updated=datetime.utcnow()
                )
                
                # Determine content type
                content_type = ContentType.WEBSITE
                if '/news/' in clean_url or '/press-releases/' in clean_url:
                    content_type = ContentType.NEWS
                elif '/blog/' in clean_url:
                    content_type = ContentType.BLOG_POST
                
                return Content(
                    url=clean_url,
                    domain=urlparse(clean_url).netloc,
                    date_added=datetime.utcnow(),
                    added_by=added_by,
                    type=content_type,
                    markdown_content=downloaded,
                    images=images,
                    links=unique_links,
                    metadata=metadata
                )
        
        except Exception as e:
            print(f"Scraping failed for {url}: {e}")
            raise

# Expose the scrape_url method at the module level for backwards compatibility
async def scrape_url(url: str, added_by: str) -> Content:
    return await ContentScraper.scrape_url(url, added_by) 