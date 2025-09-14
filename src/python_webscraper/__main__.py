from .scraper import WebScraper

START_URL = "https://os.phil-opp.com/"
OUTPUT_PATH = "html-pages"

def main() -> None:
    scraper = WebScraper(OUTPUT_PATH)
    scraper.scrapeV1(START_URL)

if __name__ == "__main__":
    main()

# It's similarly acceptable for this to live in scraper.py. It will only be executed if ran
# locally through poetry. As a module import, people will manually call
# scraper.scrape(). __main__.py is also OK to separate out.