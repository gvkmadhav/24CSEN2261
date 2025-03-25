#chatgpt
import requests
from bs4 import BeautifulSoup
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraperWithProxy:
    def __init__(self, url, proxies):
        self.url = url
        self.proxies = proxies

    def fetch_page(self):
        """Fetch a web page using a random proxy."""
        proxy = random.choice(self.proxies)
        logging.info(f"Using proxy: {proxy}")
        
        try:
            response = requests.get(self.url, proxies={"http": proxy, "https": proxy}, timeout=5)
            response.raise_for_status()
            logging.info(f"Successfully fetched page: {self.url}")
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page: {e}")
            return None

    def parse_html(self, html):
        """Parse HTML and extract data."""
        if not html:
            logging.error("No HTML to parse.")
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        logging.info(f"Page title: {title}")
        return title

   
