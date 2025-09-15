import os
import requests
import time
import asyncio
import aiohttp
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
        self.scraped = 0
        # thread pool

    def write_output_file(self, name: str, contents: str) -> None:
        host = urlparse(self.base_url).hostname
        filename = host.replace(".", "_") + "_" + name

        filepath = os.path.join(self.output_path, filename)

        with open(filepath, 'w') as f:
            f.write(contents)
        
        self.scraped += 1

    def get_child_urls(self, contents: str) -> List[str]:
        soup = BeautifulSoup(contents, 'lxml')
        href_links = [a["href"] for a in soup.find_all("a", href=True)]

        absolute_links = [link for link in href_links if is_base_http_url(link)]

        return absolute_links[:10]
    
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
        self.scrape_recursivelyV1(job, 0)

    def scrape_recursivelyV1(self, job: PageJob, level: int):
        if level > 2: 
            return

        url = job.url
        print(f"scraping: {url}")

        resp = ""
        try: 
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            # process the various status codes and errors, retry, etc.
            # retry transient errors
            print(e)
            return
            # raise

        # write to file
        filename = job.name + '.html'
        self.write_output_file(filename, resp.text)
        
        jobs = self.get_child_jobs(resp.text, job)

        for job in jobs:
            self.scrape_recursivelyV1(job, level + 1)

    def scrapeV2(self) -> None:
        asyncio.run(self.setup_loop())

    async def scrape_recursivelyV2(self, job: PageJob, level: int, sem: asyncio.Semaphore, session: aiohttp.ClientSession):
        if level > 2:
            return

        url = job.url
        print(f"scraping: {url}")

        text = ""
        async with sem:  # Use semaphore to limit concurrent requests
            try:
                # non blocking
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    resp.raise_for_status()
                    # Try to decode with UTF-8, replace invalid characters
                    content = await resp.read()
                    text = content.decode('utf-8', errors='replace')
            except Exception as e:
                # process the various status codes and errors, retry, etc.
                # retry transient errors
                print(e)
                return

        # write to file
        filename = job.name + '.html'
        
        # Consider aiofiles
        self.write_output_file(filename, text)

        jobs = self.get_child_jobs(text, job)

        # Create tasks for all child jobs and gather them
        tasks = []
        for child_job in jobs:
            task = self.scrape_recursivelyV2(child_job, level + 1, sem, session)
            tasks.append(task)

        # Wait for all child tasks to complete
        if tasks:
            await asyncio.gather(*tasks)

    async def setup_loop(self) -> None:
        sem = asyncio.Semaphore(50)  # Global semaphore to limit concurrent requests
        job = self.PageJob(self.base_url, "0")
        async with aiohttp.ClientSession() as session:
            await self.scrape_recursivelyV2(job, 0, sem, session)

def is_base_http_url(url):
    scheme = urlparse(url).scheme
    return scheme in ["http", "https"]

