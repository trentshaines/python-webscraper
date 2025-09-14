
"""
Core scraping logic for python_webscraper.
"""

START_URL = "https://example.com"


class WebScraper:
    def __init__(self) -> None:
        pass

    # recursive scrape from base url
    def scrape(self, url: str) -> None:
        print(f"scraping: {url}")
