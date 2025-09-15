from .scraper import WebScraper
import time
import os
from datetime import datetime

START_URL = "http://www.jennifer.listgarten.com/"
OUTPUT_BASE = "scraper-output"

def main() -> None:
    # Create timestamped output directories
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_v1 = os.path.join(OUTPUT_BASE, f"v1_{timestamp}")
    output_v2 = os.path.join(OUTPUT_BASE, f"v2_{timestamp}")

    os.makedirs(output_v1, exist_ok=True)

    print("Start Scraping V1 ")
    start = time.perf_counter()
    scraper = WebScraper(output_v1, START_URL)
    scraper.scrapeV1()
    end = time.perf_counter()
    print(f"Finished Scraping {scraper.scraped} Pages in {end - start:.4f} seconds")

    # os.makedirs(output_v2, exist_ok=True)
    # print("Start Scraping V2")
    # start2 = time.perf_counter()
    # scraper2 = WebScraper(output_v2, START_URL)
    # scraper2.scrapeV2()
    # end2 = time.perf_counter()
    # print(f"Finished Scraping {scraper2.scraped} Pages in {end2 - start2:.4f} seconds")

if __name__ == "__main__":
    main()

# It's similarly acceptable for this to live in scraper.py. It will only be executed if ran
# locally through poetry. As a module import, people will manually call
# scraper.scrape(). __main__.py is also OK to separate out.