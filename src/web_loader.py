import logging
import os

import requests

logger = logging.getLogger(__name__)


class WebPageLoader:
    def __init__(self, url: str):
        """
        Initializes the WebPageLoader with a specific URL.

        Args:
            url (str): The URL of the web page to be fetched.
        """
        self.url = url
        self.debug = os.getenv("DEBUG", False)

    def fetch_page(self) -> str:
        """
        Fetches a web page from the URL specified during the initialization. If in debug mode,
        it reduces the number of requests by caching the result to a local file (index.html).
        Subsequent calls read from this cached file to avoid additional requests.

        Returns:
            str: The content of the web page, either from a live fetch or from the cache.
        """
        file_path = "index.html"
        if self.debug:
            logger.warning("DEBUG mode is active!!!")
            if not os.path.exists(file_path):
                data = self.load_page()
                if data:
                    self._write_html(data, file_path)
                return data
            return self._read_html(file_path)
        return self.load_page()

    @staticmethod
    def _write_html(response: str, file_path: str):
        """
        Writes the response HTML to a local file.

        Args:
            response (str): The HTML content to be written.
            file_path (str): The path to the file where the HTML content will be saved.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)

    @staticmethod
    def _read_html(file_path: str) -> str:
        """
        Reads and returns the content of an HTML file.

        Args:
            file_path (str): The path to the file from which to read the HTML content.

        Returns:
            str: The content of the HTML file.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def load_page(self) -> str | None:
        """
        Loads a web page from the internet using HTTP GET. It uses custom headers
        to simulate a browser request.

        Returns:
            str | None: The content of the web page if the request is successful; None otherwise.
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            logger.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            logger.warning(f"An error occurred during the request: {e}")
            return None
