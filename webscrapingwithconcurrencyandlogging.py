#chatgpt
import requests
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraperError(Exception):
    """Custom exception for web scraper errors."""
    pass

class WebScraper:
    def __init__(self, base_url, max_threads=5):
        self.base_url = base_url
        self.max_threads = max_threads
        self.fetched_data = []
        
    def fetch_page(self, url):
        """Fetch the content of a web page."""
        try:
            logging.info(f"Fetching page: {url}")
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch page {url}: {e}")
            return None
    
    def parse_html(self, html):
        """Parse the HTML and extract heading tags (h1, h2, h3, etc.)."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            headings = soup.find_all(['h1', 'h2', 'h3'])
            return [heading.get_text(strip=True) for heading in headings]
        except Exception as e:
            logging.error(f"Error while parsing HTML: {e}")
            return []
    
    def save_data(self, filename='scraped_data.txt'):
        """Save the scraped data to a file."""
        try:
            with open(filename, 'w') as f:
                for item in self.fetched_data:
                    f.write(f"{item}\n")
            logging.info(f"Data saved to {filename}.")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
    
    def scrape_page(self, page_url):
        """Scrape a single page for headings."""
        html = self.fetch_page(page_url)
        if html:
            headings = self.parse_html(html)
            self.fetched_data.extend(headings)
    
    def scrape(self, page_urls):
        """Scrape multiple pages concurrently."""
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            executor.map(self.scrape_page, page_urls)
    
    def get_fetched_data(self):
        """Return the scraped data."""
        return self.fetched_data


# Example usage of WebScraper class
def main():
    # Example base URL and list of pages to scrape
    base_url = 'https://example.com'  # Replace with an actual URL you want to scrape
    page_urls = [f"{base_url}/page{i}" for i in range(1, 6)]  # List of page URLs to scrape

    scraper = WebScraper(base_url, max_threads=5)
    
    try:
        # Start scraping pages concurrently
        logging.info("Starting the scraping process...")
        scraper.scrape(page_urls)
        
        # Save the fetched data to a file
        scraper.save_data('scraped_headings.txt')
        
        # Print the fetched headings
        for data in scraper.get_fetched_data():
            print(data)
        
    except WebScraperError as e:
        logging.error(f"Web scraper error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
