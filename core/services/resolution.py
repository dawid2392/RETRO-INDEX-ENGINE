import requests
import logging
from bs4 import BeautifulSoup
from core.models import Entity, Relationship, Source
from urllib.parse import urljoin, quote, unquote

logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def fetch_url(self, url):
        """Fetch URL, extract title, meta description, and top images."""
        try:
            logger.info(f"CRAWLER: Fetching {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            title = soup.title.string.strip() if soup.title else ""
            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag.get("content", "").strip() if desc_tag else ""
            
            images = []
            for img in soup.find_all("img", limit=5):
                src = img.get("src")
                if src and not src.startswith("data:"):
                    full_src = urljoin(url, src)
                    images.append(full_src)
            
            return {"title": title, "description": description}, images
        except Exception as e:
            logger.error(f"CRAWLER ERROR: {url}: {e}")
            return None, []

    def search(self, query):
        """Perform a DuckDuckGo search."""
        search_url = f"https://duckduckgo.com/html/?q={quote(query)}"
        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            results = []
            for res in soup.find_all("div", class_="result"):
                a_tag = res.find("a", class_="result__a")
                if a_tag and a_tag.get("href"):
                    href = a_tag.get("href")
                    # Extract real URL from DDG redirection
                    url = ""
                    if "uddg=" in href:
                        url = unquote(href.split("uddg=")[1].split("&")[0])
                    else:
                        url = href
                    
                    results.append({"title": a_tag.get_text(), "url": url})
            return results
        except Exception as e:
            logger.error(f"SEARCH ERROR: {query}: {e}")
            return []

class NetworkDiscoveryService:
    @staticmethod
    def perform_osint_search(query):
        """Perform discovery using Web Crawling, extracting metadata and images."""
        crawler = WebCrawler()
        search_results = crawler.search(query)
        
        source, _ = Source.objects.get_or_create(name='Web Crawler Engine')
        person, _ = Entity.objects.get_or_create(entity_type='PERSON', value=query, source=source)
        
        # Use first valid image found among search results if available
        found_photo = None
        
        # Increase search limit to 6 and improve crawling logic
        for res in search_results[:6]:
            meta, images = crawler.fetch_url(res['url'])
            
            if images and not found_photo:
                found_photo = images[0]
            
            if meta:
                associate_val = meta['title'] or res['title']
                if associate_val and associate_val.lower() != query.lower():
                    associate, _ = Entity.objects.get_or_create(
                        entity_type='PERSON', value=associate_val[:100], source=source
                    )
                    Relationship.objects.get_or_create(
                        source_entity=person, target_entity=associate, 
                        relationship_type='ASSOCIATED_WITH', weight=0.5
                    )
        
        person.photo_url = found_photo or f"https://api.dicebear.com/7.x/initials/svg?seed={quote(query)}"
        person.save()
        return person

class EntityResolutionService:
    @staticmethod
    def resolve(data):
        query = data.get('query')
        if query:
            return NetworkDiscoveryService.perform_osint_search(query)
        return None
