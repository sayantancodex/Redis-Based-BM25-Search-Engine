import requests
from bs4 import BeautifulSoup
import redis
from urllib.parse import urljoin, urlparse

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class WebCrawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.data = []  # Temporary batch storage

    def extract_domain(self, url):
        """Extracts domain name from a URL (e.g., 'example.com')."""
        return urlparse(url).netloc

    def crawl(self, url):
        """Crawls a URL, extracts links & their alt text or inner text, and stores in Redis."""
        if len(self.visited_urls) >= self.max_pages:
            return

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return

            self.visited_urls.add(url)
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                href = urljoin(url, link["href"])  # Convert relative URLs to absolute
                domain = self.extract_domain(href)  # Extract domain name
                alt_text = link.get("alt", "").strip()  # Get 'alt' text if available
                inner_text = link.get_text(strip=True)  # Get inner text if available

                # Use alt text if available; otherwise, use inner text
                content = alt_text if alt_text else inner_text
                content = f"{content} {domain}" if content else f"No Description {domain}"

                # Append new entry
                self.data.append((href, content))
                print(f"✅ Found: {href} | Content: {content}")

                # Save to Redis every 10 crawls
                if len(self.visited_urls) % 10 == 0:
                    self.save_to_redis()
                    self.data = []  # Clear batch storage

                # Recursively crawl new pages if not visited
                if href not in self.visited_urls and len(self.visited_urls) < self.max_pages:
                    self.crawl(href)

        except requests.RequestException as e:
            print(f"❌ Failed to crawl {url}: {e}")

    def save_to_redis(self):
        """Save data batch to Redis."""
        for url, content in self.data:
            redis_client.hset("web_crawl_data", url, content)
        print(f"💾 Saved {len(self.data)} entries to Redis (Total: {len(self.visited_urls)})")

    def start(self):
        """Start crawling from the initial URL."""
        print(f"🚀 Starting crawl from: {self.start_url}")
        redis_client.delete("web_crawl_data")  # Clear old data
        self.crawl(self.start_url)
        if self.data:
            self.save_to_redis()  # Save any remaining data
        print("✅ Crawling finished! Data stored in Redis.")

# Run the crawler
crawler = WebCrawler(start_url="https://wikipedia.com", max_pages=50)
crawler.start()
