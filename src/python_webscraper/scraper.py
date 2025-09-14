import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import List


"""
Core scraping logic for python_webscraper.
"""
class WebScraper:
    class PageJob:
        url: str
        name: str # ex: 1.3.2

        def __init__(self, url: str, name: str) -> None:
            self.url = url
            self.name = name

    def __init__(self, output_path: str, base_url: str) -> None:
        self.output_path = output_path
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url

    def write_output_file(self, filename: str, contents: str) -> None:
        filepath = os.path.join(self.output_path, filename)

        with open(filepath, 'w') as f:
            f.write(contents)

    def get_child_urls(self, contents: str) -> List[str]:
        soup = BeautifulSoup(contents, 'lxml')
        href_links = [a["href"] for a in soup.find_all("a", href=True)]

        absolute_links = [link if is_base_http_url(link) else self.base_url + link for link in href_links]

        return absolute_links
    
    def get_child_jobs(self, contents: str, current_job: PageJob) -> List[str]:
        child_urls = self.get_child_urls(contents)

        child_jobs = []
        for i, url in enumerate(child_urls):
            name = current_job.name + "_" + str(i)
            child_jobs.append(self.PageJob(url, name))

        return child_jobs

    # recursive scrape from base url
    # make everything synchronous
    def scrapeV1(self) -> None:
        job = self.PageJob(self.base_url, "0")
        self.scrape_recursively(job, 0)

    def scrape_recursively(self, job: PageJob, level: int):
        if level > 2: 
            return

        url = job.url
        print(f"scraping: {url}")

        
        resp = ""
        try: 
            resp = requests.get(url)
            resp.raise_for_status()
        except Exception as e:
            # process the various status codes and errors, retry, etc.
            # retry transient errors
            print(e)
            # raise

        # write to file
        filename = job.name + '.html'
        self.write_output_file(filename, resp.text)
        
        jobs = self.get_child_jobs(resp.text, job)

        for job in jobs:
            self.scrape_recursively(job, level + 1)

def is_base_http_url(url):
    scheme = urlparse(url).scheme
    return scheme in ["http", "https"]

