"""Tests for the WebScraper class."""

import pytest
from python_webscraper.scraper import WebScraper


class TestWebScraper:
    """Test cases for WebScraper."""

    def test_init(self):
        """Test WebScraper initialization."""
        scraper = WebScraper("https://example.com")
        assert scraper.base_url == "https://example.com"

    def test_fetch_page_without_path(self):
        """Test fetching a page without a path."""
        scraper = WebScraper("https://example.com")
        result = scraper.fetch_page()
        assert result == True

