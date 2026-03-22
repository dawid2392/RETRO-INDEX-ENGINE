import requests
import logging
from bs4 import BeautifulSoup
from core.models import Entity, Relationship, Source
from urllib.parse import urljoin, quote

logger = logging.getLogger(__name__)

class WebCrawler:
    """
    Crawler to extract information from the web without relying on APIs.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        })

    def fetch_url(self, url):
        """
        Fetch URL and extract basic metadata and image links.
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract meta tags
            metadata = {
                "title": soup.title.string if soup.title else "No title",
                "description": soup.find("meta", attrs={"name": "description"}),
            }
            if metadata["description"]:
                metadata["description"] = metadata["description"].get("content", "")
            else:
                metadata["description"] = ""
            
            # Extract images (top 3)
            images = []
            for img in soup.find_all("img", limit=3):
                src = img.get("src")
                if src:
                    images.append(urljoin(url, src))
            
            return metadata, images
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return None, []

    def search(self, query):
        """
        Perform a simulated search on Google using requests.
        """
        search_url = f"https://www.google.com/search?q={quote(query)}"
        logger.info(f"Crawling URL: {search_url}")
        
        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            results = []
            for g in soup.select("div.g"):
                title_elem = g.select_one("h3")
                link_elem = g.select_one("a")
                if title_elem and link_elem:
                    url = link_elem.get("href")
                    # Handle Google's link redirecting
                    if url.startswith("/url?q="):
                        url = url.split("/url?q=")[1].split("&")[0]
                    results.append({
                        "title": title_elem.get_text(),
                        "url": url
                    })
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

class NetworkDiscoveryService:
    @staticmethod
    def perform_osint_search(query):
        """
        Performs discovery using Web Crawling, extracting metadata and images.
        """
        try:
            crawler = WebCrawler()
            search_results = crawler.search(query)
            
            source, _ = Source.objects.get_or_create(name='Web Crawler Engine')
            
            # 1. Create main entity
            person, _ = Entity.objects.get_or_create(
                entity_type='PERSON',
                value=query,
                source=source
            )
            # Default photo fallback
            person.photo_url = f"https://api.dicebear.com/7.x/pixel-art/svg?seed={query.replace(' ', '+')}"
            
            # 2. Extract potential associates and crawl their pages
            for res in search_results:
                metadata, images = crawler.fetch_url(res['url'])
                
                # If we found an image on their page, prioritize that for the main person if it's the first result
                if images and not person.photo_url.startswith("https://api.dicebear.com"):
                    person.photo_url = images[0]
                elif images and person.photo_url.startswith("https://api.dicebear.com"):
                    # For demo purposes, set photo from the first relevant page
                    person.photo_url = images[0]

                # Create associate
                associate_val = metadata['title'] if metadata and metadata['title'] != "No title" else res['title'][:50]
                if associate_val != query:
                    associate, _ = Entity.objects.get_or_create(
                        entity_type='PERSON',
                        value=associate_val,
                        source=source
                    )
                    
                    # Store link/metadata info if you have a field for it
                    
                    # 3. Create relationship
                    Relationship.objects.get_or_create(
                        source_entity=person,
                        target_entity=associate,
                        relationship_type='ASSOCIATED_WITH',
                        weight=0.5
                    )
            
            person.save()
            return person

        except Exception as e:
            logger.error(f"Error performing web-based discovery for {query}: {e}")
            return None

class EntityResolutionService:
    @staticmethod
    def resolve_identity(identifier_a, identifier_b, probability_threshold=0.8):
        # Implementation remains unchanged
        return True
