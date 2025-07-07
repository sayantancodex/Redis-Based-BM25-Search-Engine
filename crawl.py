import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.data = []  # Temporary storage for batch writing

    def extract_domain(self, url):
        """Extracts the domain name from a URL (e.g., 'example.com')."""
        return urlparse(url).netloc

    def crawl(self, url):
        """Crawl the given URL, extract links & their alt text or inner text, and store data."""
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
                self.data.append([href, content])
                print(f"📄 Crawled {len(self.visited_urls)}/{self.max_pages} pages so far")

                print(f"✅ Found: {href} | Content: {content}")

                # Save every 10 crawls
                if len(self.visited_urls) % 10 == 0:
                    self.save_to_csv()
                    self.data = []  # Clear the list after saving

                # Recursively crawl the new page if not visited
                if href not in self.visited_urls and len(self.visited_urls) < self.max_pages:
                    self.crawl(href)

        except requests.RequestException as e:
            print(f"❌ Failed to crawl {url}: {e}")

    def save_to_csv(self):
        """Append the crawled data to CSV file."""
        with open("data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
        print(f"💾 Data saved to data.csv ({len(self.visited_urls)} pages crawled)")

    def start(self):
        """Start crawling from the initial URL."""
        print(f"🚀 Starting crawl from: {self.start_url}")
        with open("data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Content"])  # Write headers
        self.crawl(self.start_url)
        if self.data:
            self.save_to_csv()  # Save any remaining data at the end
        print("✅ Crawling finished! Data saved.")

# Run the crawler
crawler = WebCrawler(start_url="https://google.com", max_pages=50)
crawler.start()
