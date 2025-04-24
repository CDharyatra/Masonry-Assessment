import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, List
import sys
import os
import re
import time

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class WebScraperTool:
    """
    Tool for scraping content from web pages.
    Extracts text, metadata, and structured data from web pages.
    """
    
    def __init__(self):
        self.user_agent = Config.USER_AGENT
        self.timeout = Config.REQUEST_TIMEOUT
        self.headers = {'User-Agent': self.user_agent}
        
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from the specified URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing the scraped content and metadata
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f"Failed to retrieve content: HTTP {response.status_code}",
                    'url': url,
                    'content': None,
                    'metadata': None
                }
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract metadata
            metadata = self._extract_metadata(soup, url)
            
            # Extract main content
            content = self._extract_content(soup)
            
            # Extract structured data if available
            structured_data = self._extract_structured_data(soup)
            
            return {
                'success': True,
                'url': url,
                'content': content,
                'metadata': metadata,
                'structured_data': structured_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url,
                'content': None,
                'metadata': None
            }
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract metadata from the web page.
        
        Args:
            soup: BeautifulSoup object of the page
            url: The URL of the page
            
        Returns:
            Dictionary containing metadata
        """
        metadata = {
            'title': None,
            'description': None,
            'keywords': None,
            'author': None,
            'published_date': None,
            'site_name': None,
            'url': url
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.text.strip()
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            # Description
            if tag.get('name') == 'description' or tag.get('property') == 'og:description':
                metadata['description'] = tag.get('content')
            
            # Keywords
            elif tag.get('name') == 'keywords':
                metadata['keywords'] = tag.get('content')
            
            # Author
            elif tag.get('name') == 'author':
                metadata['author'] = tag.get('content')
            
            # Published date
            elif tag.get('name') == 'article:published_time' or tag.get('property') == 'article:published_time':
                metadata['published_date'] = tag.get('content')
            
            # Site name
            elif tag.get('property') == 'og:site_name':
                metadata['site_name'] = tag.get('content')
        
        # If site_name is not found, extract from URL
        if not metadata['site_name']:
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                metadata['site_name'] = domain
            except:
                pass
        
        return metadata
    
    def _extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract main content from the web page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Dictionary containing extracted content
        """
        content = {
            'main_text': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': []
        }
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Extract headings
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        content['headings'] = headings
        
        # Extract paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text:
                paragraphs.append(text)
        content['paragraphs'] = paragraphs
        
        # Extract links
        links = []
        for a in soup.find_all('a', href=True):
            link_text = a.get_text().strip()
            if link_text:
                links.append({
                    'text': link_text,
                    'href': a['href']
                })
        content['links'] = links
        
        # Extract images with alt text
        images = []
        for img in soup.find_all('img', alt=True):
            if img.get('src'):
                images.append({
                    'src': img['src'],
                    'alt': img['alt']
                })
        content['images'] = images
        
        # Combine all paragraph text for main_text
        content['main_text'] = '\n\n'.join(paragraphs)
        
        # Try to identify and extract the main article content
        article = soup.find('article')
        if article:
            article_text = article.get_text().strip()
            if len(article_text) > len(content['main_text']):
                content['main_text'] = article_text
        
        # If main_text is still empty, get all text
        if not content['main_text']:
            content['main_text'] = soup.get_text().strip()
        
        # Limit content length if needed
        if len(content['main_text']) > Config.MAX_CONTENT_LENGTH:
            content['main_text'] = content['main_text'][:Config.MAX_CONTENT_LENGTH] + "..."
        
        return content
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract structured data (JSON-LD) from the web page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of structured data objects
        """
        structured_data = []
        
        # Look for JSON-LD scripts
        ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data.append(data)
            except:
                continue
        
        return structured_data
    
    def scrape_multiple_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape content from multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of dictionaries containing scraped content
        """
        results = []
        
        for url in urls:
            # Add a small delay between requests to be respectful
            time.sleep(1)
            result = self.scrape_url(url)
            results.append(result)
        
        return results
