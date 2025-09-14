import os
import requests

"""
Core scraping logic for python_webscraper.
"""
class WebScraper:
    class PageJob:
        url: str
        job_name: str # ex: 1.3.2

    def __init__(self, output_path: str) -> None:
        self.output_path = output_path

    def write_output_file(self, filename: str, contents: str) -> None:
        filepath = os.path.join(self.output_path, filename)

        with open(filepath, 'w') as f:
            f.write(contents)

    # recursive scrape from base url
    # make everything synchronous
    def scrapeV1(self, url: str) -> None:
        print(f"scraping: {url}")

        try: 
            resp = requests.get(url)
            resp.raise_for_status()
        except:
            # process the various status codes and errors, retry, etc.
            # retry transient errors
            raise

        print(self.output_path)
        print("status: ", resp.status_code)

        # write to file
        self.write_output_file('first.html', resp.text)
        
        # find neighbors
        # parse for <link?>
