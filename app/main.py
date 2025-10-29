from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from crawler import crawl_regulations
from database import init_db, save_regulations, get_latest

app = FastAPI(title="RegWatcher – Regulatory Monitor")

#@app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

@app.get("/")
def home():
    return {"message": "Welcome to RegWatcher API"}

@app.get("/regulations")
def list_regulations():
    return get_latest()

@app.post("/regulations/update")
async def update_regulations():
    data = await crawl_regulations()
    save_regulations(data)
    return {"added": len(data)}