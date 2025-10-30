import aiohttp
import asyncio
from bs4 import BeautifulSoup
from hashlib import md5
from datetime import datetime
from app.config import load_config

#BASE_URL = "https://www.eba.europa.eu/publications-and-media/publications"

async def fetch_html(session, url):
    async with session.get(url, timeout=20) as resp:
        return await resp.text()

async def crawl_single_page(session, url, source_name, page=None):
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for a in soup.select("a"):
        text = a.text.strip()
        href = a.get("href", "")
        if text and href and "guideline" in text.lower():
            if href.startswith("/"):
                href = url.rstrip("/") + href
            results.append({
                "source": source_name,
                "title": text,
                "url": href,
                "hash": md5(href.encode()).hexdigest(),
                "date": datetime.utcnow().isoformat(),
            })
    return results

async def crawl_auto_paginate(session, base_url, source_name):
    all_results = []
    next_url = base_url
    page = 1

    while next_url:
        print(f"Crawling {source_name} page {page}: {next_url}")
        html = await fetch_html(session, next_url)
        soup = BeautifulSoup(html, "html.parser")

        # collect links from the current page
        all_results += await crawl_single_page(session, next_url, source_name, page)

        # find the link of the next page if exists
        nxt= soup.select_one('a[rel="next"]')
        if nxt and nxt.get("href"):
            next_url = next_url + nxt["href"]
            page += 1
        else:
            next_url = None

    return all_results

async def crawl_fixed_pages(session, base_url, source_name, max_pages=1):
    all_results = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}"
        print(f"Crawling {source_name} page {page}/{max_pages}: {url}")
        all_results += await crawl_single_page(session, url, source_name, page)
    return all_results

async def crawl_regulations():
    config = load_config()
    all_results = []

    async with aiohttp.ClientSession() as session:
        for src in config["sources"]:
            name = src["name"]
            url = src["url"]
            auto = src.get("auto_paginate", False)
            max_pages = src.get("max_pages", 1)

            if auto:
                all_results += await crawl_auto_paginate(session, url, name)
            else:
                all_results += await crawl_fixed_pages(session, url, name, max_pages)
    return all_results

if __name__ == "__main__":
    data = asyncio.run(crawl_regulations())
    for d in data:
        print(d)