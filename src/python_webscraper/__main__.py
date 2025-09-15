from .scraper import WebScraper
import time

START_URL = "http://www.jennifer.listgarten.com/"
OUTPUT_PATH = "html-pages"
OUTPUT_PATH_ASYNC = "html-pages-async"

def main() -> None:
    print("Start Scraping V1 ")
    start = time.perf_counter()
    scraper = WebScraper(OUTPUT_PATH, START_URL)
    scraper.scrapeV1()
    end = time.perf_counter()
    print(f"Finished Scraping {scraper.scraped} Pages in {end - start:.4f} seconds")

    # print("Start Scraping V2")
    # start2 = time.perf_counter()
    # scraper2 = WebScraper(OUTPUT_PATH_ASYNC, START_URL)
    # scraper2.scrapeV2()
    # end2 = time.perf_counter()
    # print(f"Finished Scraping {scraper2.scraped} Pages in {end2 - start2:.4f} seconds")

if __name__ == "__main__":
    main()

# It's similarly acceptable for this to live in scraper.py. It will only be executed if ran
# locally through poetry. As a module import, people will manually call
# scraper.scrape(). __main__.py is also OK to separate out.