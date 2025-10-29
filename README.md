# RegWatcher – Simplified RegTech Compliance Monitor

**RegWatcher** is a lightweight RegTech demo project that automatically monitors regulatory websites (e.g., European Banking Authority) and exposes a simple REST API for compliance teams to track and query new publications.

This project showcases how **automation, data pipelines, and compliance monitoring** can work together to improve regulatory oversight — a key concept in RegTech.

## Features
- ✅ Asynchronous web crawler (Python + aiohttp)
- 🧩 FastAPI REST interface
- 💾 Local SQLite database
- ⚙️ One-click update endpoint
- 🐳 Easily deployable with Docker

## Tech Stack
- Python 3.12
- FastAPI
- aiohttp
- BeautifulSoup4
- SQLite

## Run locally
```bash
uvicorn app.main:app --reload