from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from app.crawler import crawl_regulations
from app.database import init_db, save_regulations, get_latest, reset_regulations_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()  
    yield       
    print("Shutting down...")

app = FastAPI(title="RegWatcher: Regulatory Monitor", lifespan=lifespan)

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

@app.post("/regulations/reset")
def reset_table():
    reset_regulations_table()
    return {"message": "Table 'regulations' dropped and recreated successfully."}