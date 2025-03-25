#Chatgpt
import requests
import logging
import time
from requests.exceptions import HTTPError, Timeout, RequestException

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class APIClientError(Exception):
    """Custom exception for API client errors."""
    pass

class APIClient:
    def __init__(self, base_url, max_retries=3, timeout=5):
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout

    def send_request(self, endpoint):
        """Send a GET request to the given endpoint."""
        url = f"{self.base_url}/{endpoint}"
        attempt = 0
        while attempt < self.max_retries:
            try:
                logging.info(f"Sending request to {url}, Attempt {attempt + 1}...")
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                return response.json()  # Return the JSON data from the API
            except Timeout:
                logging.error(f"Timeout error while accessing {url}. Retrying...")
            except HTTPError as http_err:
                logging.error(f"HTTP error occurred: {http_err}. Retrying...")
            except RequestException as err:
                logging.error(f"Error occurred: {err}. Retrying...")
            time.sleep(2)  # Wait before retrying
            attempt += 1
        raise APIClientError(f"Failed to fetch data from {url} after {self.max_retries} retries.")

    def get_data(self, endpoint):
        """Retrieve data from an API endpoint."""
        try:
            data = self.send_request(endpoint)
            logging.info(f"Data retrieved from {endpoint}: {data}")
            return data
        except APIClientError as e:
            logging.error(f"API client error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None

# Example usage
def main():
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    # Attempt to get data from an API endpoint
    data = client.get_data("posts/1")
    
    if data:
        logging.info("Successfully retrieved data!")
        print(data)
    else:
        logging.error("Failed to retrieve data.")

if __name__ == "__main__":
    main()
