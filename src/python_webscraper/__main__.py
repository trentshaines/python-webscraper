from .scraper import WebScraper, START_URL


def main() -> None:
    scraper = WebScraper()
    scraper.scrape(START_URL)


if __name__ == "__main__":
    main()

