import aiohttp
import asyncio
from bs4 import BeautifulSoup
from hashlib import md5
from datetime import datetime

BASE_URL = "https://www.eba.europa.eu/regulation-and-policy"

async def fetch_html(session, url):
    async with session.get(url, timeout=20) as resp:
        return await resp.text()

async def crawl_regulations():
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, BASE_URL)
        soup = BeautifulSoup(html, "html.parser")

        results = []
        for a in soup.select("a"):
            text = a.text.strip()
            href = a.get("href", "")
            if text and "guideline" in text.lower() and href.startswith("/"):
                full_url = f"https://www.eba.europa.eu{href}"
                item = {
                    "title": text,
                    "url": full_url,
                    "hash": md5(full_url.encode()).hexdigest(),
                    "date": datetime.utcnow().isoformat()
                }
                results.append(item)
        return results

if __name__ == "__main__":
    data = asyncio.run(crawl_regulations())
    for d in data:
        print(d)